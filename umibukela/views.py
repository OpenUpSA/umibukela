from collections import Counter
from datetime import datetime
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.http import HttpResponse, Http404, JsonResponse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils.text import slugify
from itertools import groupby
from kobo import Kobo
from wkhtmltopdf.utils import wkhtmltopdf
from wkhtmltopdf.views import PDFResponse
from xform import map_questions, field_per_SATA_option, skipped_as_na
import analysis
import json
import os
import pandas
import re
import requests
import csv
import csv_export

from .forms import CRSFromKoboForm
from .models import (Cycle, CycleResultSet, Partner, Programme,
                     ProgrammeKoboRefreshToken, Province, Site, Submission,
                     Survey, SurveyKoboProject, SurveyType,
                     UserKoboRefreshToken, ProgrammeStory, ProgrammeImage,
                     ProgrammeResources, SurveyTypeData)

IGNORE_TYPES = ['start', 'end', 'meta', 'today', 'username', 'phonenumber']
TRIM_SITE_RE = r"SASSA Service Office: |SASSA Pay Point: "
TRIM_TYPE_RE = r" - Citizen"


def home(request):
    survey_types = SurveyType.objects.filter(public=True).all()
    return render(request, 'index.html', {
        'active_tab': 'home',
        'survey_types': survey_types,
    })


def about(request):
    return render(request, 'about.html', {
        'active_tab': 'about',
    })


def learn(request):
    return render(request, 'learn.html', {
        'active_tab': 'learn',
    })


def resources(request):
    return render(request, 'resources.html', {
        'active_tab': 'resources',
    })


def programmes(request):
    prog = Programme\
           .objects\
           .all()\
           .order_by('long_name')\
           .prefetch_related('program_image')
    return render(request, 'programmes.html', {'programmes': prog})


def get_submission_count(request, programme_slug, cycle_id):
    surveys = Survey\
              .objects\
              .filter(cycle__programme__slug=programme_slug, cycle_id=cycle_id)
    survey_submission_count = sum(
        survey.get_submission_count() for survey in surveys)

    return JsonResponse({'submission_count': survey_submission_count})


def get_datastudio_cycle(request, programme_slug, cycle_id):
    data_results = SurveyTypeData\
                   .objects\
                   .filter(cycle_id=cycle_id)\
                   .values('datastudio', 'survey__name')
    return JsonResponse({
        'datastudio':
        {key['survey__name']: key['datastudio']
         for key in data_results}
    })


def get_community_cycle(request, programme_slug, cycle_id):
    partners = CycleResultSet\
               .objects\
               .filter(survey__cycle__programme__slug=programme_slug,
                       survey__cycle_id=cycle_id)\
               .order_by('partner__id')\
               .distinct('partner')\
               .select_related('partner')\
               .only('partner')
    cycle_partners = [{
        'name':
        p.partner.full_name,
        'site':
        p.site.name,
        'total':
        p.summary()['total'],
        'url':
        '/sites/{}/results/{}'.format(
            p.partner.latest_complete_result().site.slug,
            p.partner.latest_complete_result().id)
    } for p in partners]

    return JsonResponse({'partners': cycle_partners})


def programme_result_cycle(request, programme_slug, cycle_id):
    """
    Get the results for a programme for a particular cycle
    """
    surveys = Survey\
              .objects\
              .filter(cycle__programme__slug=programme_slug, cycle_id=cycle_id)
    survey_submission_count = sum(
        survey.get_submission_count() for survey in surveys)
    data_results = SurveyTypeData\
                   .objects\
                   .filter(cycle_id=cycle_id)\
                   .values('datastudio', 'survey__name')
    partners = CycleResultSet\
               .objects\
               .filter(survey__cycle__programme__slug=programme_slug,
                       survey__cycle_id=cycle_id)\
               .order_by('partner__id')\
               .distinct('partner')\
               .select_related('partner')\
               .only('partner')
    cycle_partners = [{
        'name':
        p.partner.full_name,
        'site':
        p.site.name,
        'total':
        p.summary()['total'],
        'url':
        '/sites/{}/results/{}'.format(
            p.partner.latest_complete_result().site.slug,
            p.partner.latest_complete_result().id)
    } for p in partners]
    return JsonResponse({
        'submission_count': survey_submission_count,
        'datastudio':
        {key['survey__name']: key['datastudio']
         for key in data_results},
        'partners': cycle_partners
    })


def programme_detail(request, programme_slug):
    programme = Programme.objects.get(slug=programme_slug)
    surveys = Survey.objects.filter(cycle__programme__slug=programme_slug)
    survey_submission_count = sum(
        survey.get_submission_count() for survey in surveys)
    stories = ProgrammeStory.objects.filter(programme__slug=programme_slug)[:2]
    programme_cycles = Cycle\
                       .objects\
                       .filter(programme__slug=programme_slug)\
                       .only('start_date', 'end_date')\
                       .order_by('start_date')
    latest_programme_cycle = programme_cycles.last()

    type_surveys = Survey\
                   .objects\
                   .filter(cycle__programme__slug=programme_slug)\
                   .distinct('type')\
                   .order_by('type__id')\
                   .only('type')\
                   .values('type', 'type__slug', 'type__name')
    survey_ids = [t['type'] for t in type_surveys]
    data_results = SurveyTypeData\
                   .objects\
                   .filter(survey__id__in=survey_ids,
                           cycle=latest_programme_cycle)
    programme_images = ProgrammeImage\
                       .objects\
                       .filter(programme__slug=programme_slug)\
                       .exclude(featured=True)[:4]
    try:
        featured_image = ProgrammeImage\
                         .objects\
                         .only('image')\
                         .get(programme__slug=programme_slug,
                              featured=True)
    except ProgrammeImage.DoesNotExist:
        featured_image = False

    partners = CycleResultSet\
               .objects\
               .filter(survey__cycle__programme__slug=programme_slug,
                       survey__cycle=latest_programme_cycle)\
               .order_by('partner__id')\
               .distinct('partner')\
               .select_related('partner')\
               .only('partner')
    donars = CycleResultSet\
              .objects\
              .filter(survey__cycle__programme__slug=programme_slug)\
              .exclude(funder__isnull=True)\
              .distinct('funder')\
              .order_by('funder')\
              .select_related('funder')\
              .only('funder')
    resources = ProgrammeResources\
                .objects\
                .filter(programme__slug=programme_slug)\
                .select_related('resource')\
                .order_by('order')
    return render(
        request, 'programme_detail.djhtml', {
            'programme': programme,
            'programme_cycles': programme_cycles,
            'latest_cycle': latest_programme_cycle,
            'survey_submissions': survey_submission_count,
            'partners': partners,
            'donars': donars,
            'stories': stories,
            'programme_images': programme_images,
            'resources': resources,
            'featured_image': featured_image,
            'datastudio': data_results,
            'surveys': type_surveys
        })


def progamme_survey(request, survey_name):
    """
    Show all the sites that were in a survey
    """
    try:
        survey = Survey.objects.get(name=survey_name)
    except Survey.DoesNotExist:
        raise Http404
    else:
        cycle_result_set = CycleResultSet.objects.filter(survey=survey)
        return render(request, 'programme_survey.html', {
            'cycle_result_set': cycle_result_set,
            'survey': survey
        })


def programme_story(request, programme_slug):
    """
    Show all the stories for a programme
    """
    programme = Programme.objects.get(slug=programme_slug)
    stories = ProgrammeStory.objects.all()
    return render(request, 'programme_stories.html', {
        'stories': stories,
        'programme': programme
    })


def story_detail(request, story_slug):
    """
    show all the detail and images for a story
    """
    story = ProgrammeStory\
            .objects\
            .select_related('programme')\
            .get(slug=story_slug)
    more_stories = ProgrammeStory\
                   .objects\
                   .filter(programme=story.programme)\
                   .exclude(slug=story_slug)
    return render(request, 'story_detail.html', {
        'story': story,
        'more_stories': more_stories
    })


def site_survey_download(request, cycle_result_id):
    """
    Download a survey from a site
    """
    survey = CycleResultSet\
             .objects\
             .only('survey')\
             .get(id=cycle_result_id)
    submission = Submission.objects.filter(cycle_result_set=cycle_result_id)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachement;filename=export.csv'
    frame = pandas.DataFrame()
    for answer in submission:
        row = csv_export.export_row(answer, survey.form)
        frame = frame.append(row, ignore_index=True)
    frame.to_csv(response, index=False, encoding='utf-8')
    return response


def survey_download(requests, survey_name):
    """
    Download all the survey data from all the sites
    """
    survey = Survey.objects.get(name=survey_name)
    submissions = Submission\
                  .objects\
                  .filter(cycle_result_set__survey__name=survey_name)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachement;filename=export.csv'
    frame = pandas.DataFrame()
    fields = csv_export.form_questions(survey.form)
    writer = csv.DictWriter(response, fieldnames=fields.keys())
    writer.writeheader()
    for answer in submissions:
        row = csv_export.export_row(answer, fields)
        writer.writerow(row)
        #frame = frame.append(row, ignore_index=True)
    #frame.to_csv(response, index=False, encoding='utf-8')
    return response


def sites(request):
    sites = Site.objects.all().prefetch_related('province', 'sector')

    return render(request, 'sites.html', {
        'active_tab': 'sites',
        'sites': sites,
    })


def site(request, site_slug):
    site = get_object_or_404(Site, slug=site_slug)
    programmes = site.programmes()
    return render(request, 'site_detail.html', {
        'active_tab': 'sites',
        'site': site,
        'programmes': programmes
    })


def site_result(request, site_slug, result_id):
    result_set = get_object_or_404(
        CycleResultSet, id=result_id, site__slug__exact=site_slug)
    if not (result_set.published or request.user.is_superuser):
        raise Http404("No such CycleResultSet found")
    form, responses = result_set.get_survey()
    if responses:
        df = pandas.DataFrame(responses)
        site_totals = analysis.count_submissions(df)
        site_results = analysis.count_options(df, form['children'])
        site_results = analysis.calc_q_percents(site_results)
        prev_result_set = result_set.get_previous()
        if prev_result_set:
            prev_form, prev_responses = prev_result_set.get_survey()
            if prev_responses:
                site_totals = analysis.count_submissions(
                    pandas.DataFrame(responses + prev_responses))
                prev_df = pandas.DataFrame(prev_responses)
                prev_results = analysis.count_options(prev_df,
                                                      prev_form['children'])
                prev_results = analysis.calc_q_percents(prev_results)
            else:
                prev_results = None
        else:
            prev_results = None
        analysis.combine_curr_hist(site_results, prev_results)
    else:
        site_totals = {'male': 0, 'female': 0, 'total': 0}
        site_results = None

    return render(
        request, 'site_result_detail.html', {
            'active_tab': 'sites',
            'result_set': result_set,
            'results': {
                'questions_dict': site_results,
                'totals': site_totals,
            }
        })


def summary(request, site_slug, result_id):
    result_set = get_object_or_404(
        CycleResultSet, id=result_id, site__slug__exact=site_slug)
    # Multiple choice question responses
    form, responses = result_set.get_survey()
    gender_disagg = not not form.get_by_path('demographics_group/gender')
    if responses:
        df = pandas.DataFrame(responses)
        site_totals = analysis.count_submissions(
            df, gender_disagg=gender_disagg)
        site_results = analysis.count_options(
            df, form['children'], gender_disagg=gender_disagg)
        site_results = analysis.calc_q_percents(site_results, gender_disagg)
        prev_result_set = result_set.get_previous()
        if prev_result_set:
            prev_form, prev_responses = prev_result_set.get_survey()
            if prev_responses:
                site_totals = analysis.count_submissions(
                    pandas.DataFrame(responses + prev_responses),
                    gender_disagg=gender_disagg)
                prev_df = pandas.DataFrame(prev_responses)
                prev_results = analysis.count_options(
                    prev_df,
                    prev_form['children'],
                    gender_disagg=gender_disagg)
                prev_results = analysis.calc_q_percents(
                    prev_results, gender_disagg)
            else:
                prev_results = None
        else:
            prev_results = None
        analysis.combine_curr_hist(site_results, prev_results)
    else:
        site_totals = {'male': 0, 'female': 0, 'total': 0}
        site_results = None
    # Text questions
    skip_questions = [
        'surveyor',
        'capturer',
    ]
    text_questions = {}
    for child in result_set.survey.form.get('children'):
        if child.get(
                'type',
                None) == 'text' and child.get('name') not in skip_questions:
            comments = Counter([
                s.answers.get(child['name'], None)
                for s in result_set.submissions.all()
            ])
            comments.pop(None, None)
            comments.pop('n/a', None)

            text_questions[child.get('name')] = {
                'label': child.get('label'),
                'comments': comments,
                'count': sum(comments.values()),
            }
    return render(
        request, 'print-materials/site_cycle_summary.html', {
            'ignore_paths': ['facility', 'demographics_group/gender'],
            'ignore_types': IGNORE_TYPES,
            'multiple_choice_types': ['select all that apply', 'select one'],
            'form': form,
            'text_questions': text_questions,
            'location_name': result_set.site.name,
            'survey_type': result_set.survey.type,
            'cycle': result_set.survey.cycle,
            'gender_disagg': gender_disagg,
            'result_set': result_set,
            'results': {
                'questions_dict': site_results,
                'totals': site_totals,
            }
        })


def summary_pdf(request, site_slug, result_id):
    result_set = get_object_or_404(
        CycleResultSet,
        id=result_id,
    )
    # render poster as pdf
    url = reverse(
        'site-result-summary',
        kwargs={
            'site_slug': site_slug,
            'result_id': result_id
        })
    url = request.build_absolute_uri(url)
    pdf = wkhtmltopdf(
        url, **{
            'margin-top': '0.5cm',
            'margin-right': '0.5cm',
            'margin-bottom': '0.5cm',
            'margin-left': '0.5cm',
        })
    filename = (u'Summary for %s - %s - %s.pdf' %
                (result_set.survey.name, result_set.partner.short_name,
                 result_set.site.name)).encode('ascii', 'ignore')
    return PDFResponse(pdf, filename=filename, show_content_in_browser=True)


def poster(request, site_slug, result_id):
    result_set = get_object_or_404(
        CycleResultSet, id=result_id, site__slug__exact=site_slug)
    form, responses = result_set.get_survey()
    totals = {
        'current': {
            'male': 0,
            'female': 0,
            'total': 0
        },
        'previous': {
            'male': 0,
            'female': 0,
            'total': 0
        },
    }
    site_results = None

    if responses:
        df = pandas.DataFrame(responses)
        totals['current'] = analysis.count_submissions(df)
        site_results = analysis.count_options(df, form['children'])
        site_results = analysis.calc_q_percents(site_results)
        prev_result_set = result_set.get_previous()
        if prev_result_set:
            prev_form, prev_responses = prev_result_set.get_survey()
            if prev_responses:
                totals['previous'] = analysis.count_submissions(
                    pandas.DataFrame(prev_responses))
                prev_df = pandas.DataFrame(prev_responses)
                prev_results = analysis.count_options(prev_df,
                                                      prev_form['children'])
                prev_results = analysis.calc_q_percents(prev_results)
                prev_date = prev_result_set.survey.cycle.start_date
            else:
                prev_results = None
                prev_date = None
        else:
            prev_results = None
            prev_date = None
        analysis.combine_curr_hist(site_results, prev_results)

    return render(
        request, result_set.survey.type.poster_template, {
            'DEBUG': settings.DEBUG,
            'form': form,
            'layout_class': slugify(result_set.survey.type.name),
            'prev_date': prev_date,
            'start_date': result_set.survey.cycle.start_date,
            'end_date': result_set.survey.cycle.end_date,
            'questions_dict': site_results,
            'sector': result_set.site.sector.name,
            'location': result_set.site.name,
            'totals': totals,
            'funder_name': result_set.funder.name,
            'partner_name': result_set.partner.full_name,
        })


def poster_pdf(request, site_slug, result_id):
    result_set = get_object_or_404(
        CycleResultSet, id=result_id, site__slug__exact=site_slug)
    # render poster as pdf
    url = reverse(
        'site-result-poster',
        kwargs={
            'site_slug': site_slug,
            'result_id': result_id
        })
    url = request.build_absolute_uri(url)
    pdf = wkhtmltopdf(
        url, **{
            'margin-top': '0.5cm',
            'margin-right': '0.5cm',
            'margin-bottom': '0.5cm',
            'margin-left': '0.5cm',
            'page-size': 'A4',
        })
    filename = (u'Poster for %s - %s - %s.pdf' %
                (result_set.survey.name, result_set.partner.short_name,
                 result_set.site.name)).encode('ascii', 'ignore')
    return PDFResponse(pdf, filename=filename, show_content_in_browser=True)


def handout(request, site_slug, result_id):
    result_set = get_object_or_404(
        CycleResultSet, id=result_id, site__slug__exact=site_slug)
    prev_result_set = result_set.get_previous()
    form, responses = result_set.get_survey()

    context = {
        'result_set': result_set,
        'questions_dict': [],
        'partner': result_set.partner,
        'site': result_set.site.name,
        'survey_type': result_set.survey.type.id,
        'prev_date': None,
        'totals': {
            'male': 0,
            'female': 0,
            'total': 0
        },
        'DEBUG': settings.DEBUG,
    }

    if prev_result_set:
        context['prev_date'] = prev_result_set.survey.cycle.start_date

    if responses:
        df = pandas.DataFrame(responses)
        site_results = analysis.count_options(df, form['children'])
        analysis.combine_curr_hist(site_results, None)

        context['questions_dict'] = site_results
        context['totals'] = analysis.count_submissions(
            pandas.DataFrame(responses))

    return render(request, 'print-materials/handouts/handout_layout.html',
                  context)


def handout_pdf(request, site_slug, result_id):
    result_set = get_object_or_404(
        CycleResultSet, id=result_id, site__slug__exact=site_slug)
    # render handout as pdf
    url = reverse(
        'site-result-handout',
        kwargs={
            'site_slug': site_slug,
            'result_id': result_id
        })
    url = request.build_absolute_uri(url)
    pdf = wkhtmltopdf(
        url, **{
            'margin-top': '0.5cm',
            'margin-right': '0.5cm',
            'margin-bottom': '0.5cm',
            'margin-left': '0.5cm',
            'page-size': 'A3',
            'orientation': 'landscape',
        })
    filename = (u'Handout for %s - %s - %s.pdf' %
                (result_set.survey.name, result_set.partner.short_name,
                 result_set.site.name)).encode('ascii', 'ignore')
    return PDFResponse(pdf, filename=filename, show_content_in_browser=True)


def comments(request, site_slug, result_id):
    result_set = get_object_or_404(
        CycleResultSet, id=result_id, site__slug__exact=site_slug)
    form, responses = result_set.get_survey()
    gender_disagg = not not form.get_by_path('demographics_group/gender')
    if responses:
        df = pandas.DataFrame(responses)
        site_totals = analysis.count_submissions(
            df, gender_disagg=gender_disagg)
    else:
        site_totals = {'male': 0, 'female': 0, 'total': 0}
    skip_questions = [
        'surveyor',
        'capturer',
    ]
    text_questions = {}
    for child in result_set.survey.form.get('children'):
        if child.get(
                'type',
                None) == 'text' and child.get('name') not in skip_questions:
            comments = Counter([
                s.answers.get(child['name'], None)
                for s in result_set.submissions.all()
            ])
            comments.pop(None, None)
            comments.pop('n/a', None)

            text_questions[child.get('name')] = {
                'label': child.get('label'),
                'comments': comments,
                'count': sum(comments.values()),
            }
    return render(
        request, 'print-materials/site_cycle_summary.html', {
            'ignore_paths': ['facility'],
            'ignore_types': IGNORE_TYPES,
            'multiple_choice_types': ['select all that apply', 'select one'],
            'form': form,
            'text_questions': text_questions,
            'location_name': result_set.site.name,
            'survey_type': result_set.survey.type,
            'cycle': result_set.survey.cycle,
            'gender_disagg': gender_disagg,
            'result_set': result_set,
            'results': {
                'questions_dict': None,
                'totals': site_totals,
            }
        })


def comments_pdf(request, site_slug, result_id):
    result_set = get_object_or_404(
        CycleResultSet, id=result_id, site__slug__exact=site_slug)
    # render poster as pdf
    url = reverse(
        'site-result-comments',
        kwargs={
            'site_slug': site_slug,
            'result_id': result_id
        })
    url = request.build_absolute_uri(url)
    pdf = wkhtmltopdf(
        url, **{
            'margin-top': '0.5cm',
            'margin-right': '0.5cm',
            'margin-bottom': '0.5cm',
            'margin-left': '0.5cm',
        })
    filename = (u'Comments for %s - %s - %s.pdf' %
                (result_set.survey.name, result_set.partner.short_name,
                 result_set.site.name)).encode('ascii', 'ignore')
    return PDFResponse(pdf, filename=filename, show_content_in_browser=True)


def partners(request):
    partners = Partner.objects.all()
    return render(request, 'partners.html', {
        'active_tab': 'partners',
        'partners': partners,
    })


def partner(request, partner_slug):
    partner = get_object_or_404(Partner, slug=partner_slug)
    return render(request, 'partner_detail.html', {
        'active_tab': 'partners',
        'partner': partner,
    })


def survey_types(request):
    survey_types = SurveyType.objects.filter(public=True).all()
    return render(
        request, 'survey_types.html', {
            'active_tab': 'surveys',
            'survey_types': survey_types,
            'username': settings.BLACKSASH_KOBO_USERNAME,
            'password': settings.BLACKSASH_KOBO_PASSWORD,
        })


def survey_type(request, survey_type_slug):
    survey_type = get_object_or_404(SurveyType, slug=survey_type_slug)
    cycles = list(
        Survey.objects.values(
            'cycle__name', 'cycle__id', 'cycle__start_date',
            'cycle__end_date').filter(
                type=survey_type).order_by('cycle__id').distinct('cycle'))
    cycles = sorted(cycles, key=lambda x: x['cycle__start_date'])
    latest_cycle = Cycle.objects.get(id=cycles[-1]['cycle__id'])
    latest_cycle_resultset = CycleResultSet.objects.filter(
        survey__cycle=latest_cycle, survey__type=survey_type).values(
            'id',
            'survey__type__id',
            'partner_id',
            'site_id',
        )
    total_count = Submission.objects.filter(
        cycle_result_set__survey__cycle=latest_cycle,
        cycle_result_set__survey__type=survey_type).values(
            'cycle_result_set__site__province__name')
    province_count = list(
        Submission.objects.filter(
            cycle_result_set__survey__cycle=latest_cycle,
            cycle_result_set__survey__type=survey_type).values(
                'cycle_result_set__site__province__slug',
                'cycle_result_set__site__province__id',
                'cycle_result_set__site__province__name').annotate(
                    dcount=Count('cycle_result_set__site__province__name')))
    for province in province_count:
        site_count = Submission.objects.filter(
            cycle_result_set__survey__cycle=latest_cycle,
            cycle_result_set__survey__type=survey_type,
            cycle_result_set__site__province__id=province[
                'cycle_result_set__site__province__id'],
        ).values('cycle_result_set__id', 'cycle_result_set__site',
                 'cycle_result_set__site__slug',
                 'cycle_result_set__site__telephone',
                 'cycle_result_set__site__name').annotate(
                     dcount=Count('cycle_result_set__site'))
        province['sites'] = site_count

    return render(
        request, 'survey_type_detail.html', {
            'active_tab': 'surveys',
            'survey_type': survey_type,
            'cycles': cycles,
            'latest_cycle': latest_cycle,
            'total_count': total_count,
            'province_count': province_count,
            'latest_cycle_resultset': latest_cycle_resultset,
            'username': settings.BLACKSASH_KOBO_USERNAME,
            'password': settings.BLACKSASH_KOBO_PASSWORD,
        })


def survey_type_cycle(request, survey_type_slug, cycle_id):
    survey_type = get_object_or_404(SurveyType, slug=survey_type_slug)
    this_cycle = get_object_or_404(Cycle, id=cycle_id)

    survey_type = get_object_or_404(SurveyType, slug=survey_type_slug)
    cycles = list(
        Survey.objects.values(
            'cycle__name', 'cycle__id', 'cycle__start_date',
            'cycle__end_date').order_by('cycle__id').distinct('cycle').filter(
                type=survey_type))
    cycles = sorted(cycles, key=lambda x: x['cycle__start_date'])
    this_cycle_resultset = CycleResultSet.objects.filter(
        survey__cycle=this_cycle, survey__type=survey_type).values(
            'id',
            'survey__type_id',
            'partner_id',
            'site_id',
        )
    total_count = Submission.objects.filter(
        cycle_result_set__survey__cycle=this_cycle,
        cycle_result_set__survey__type=survey_type).values(
            'cycle_result_set__site__province__name')
    province_count = list(
        Submission.objects.filter(
            cycle_result_set__survey__cycle=this_cycle,
            cycle_result_set__survey__type=survey_type).values(
                'cycle_result_set__site__province__slug',
                'cycle_result_set__site__province__id',
                'cycle_result_set__site__province__name').annotate(
                    dcount=Count('cycle_result_set__site__province__name')))
    for province in province_count:
        site_count = Submission.objects.filter(
            cycle_result_set__survey__cycle=this_cycle,
            cycle_result_set__survey__type=survey_type,
            cycle_result_set__site__province__id=province[
                'cycle_result_set__site__province__id'],
        ).values('cycle_result_set__id', 'cycle_result_set__site',
                 'cycle_result_set__site__telephone',
                 'cycle_result_set__site__slug',
                 'cycle_result_set__site__name').annotate(
                     dcount=Count('cycle_result_set__site'))
        province['sites'] = site_count

    return render(
        request, 'survey_type_detail_cycle.html', {
            'active_tab': 'surveys',
            'survey_type': survey_type,
            'cycles': cycles,
            'this_cycle': this_cycle,
            'total_count': total_count,
            'province_count': province_count,
            'this_cycle_resultset': this_cycle_resultset,
            'username': settings.BLACKSASH_KOBO_USERNAME,
            'password': settings.BLACKSASH_KOBO_PASSWORD,
        })


def survey_from_kobo(request):
    if not is_kobo_authed(request):
        return start_kobo_oauth(request)
    else:
        headers = {
            'Authorization':
            "Bearer %s" % request.session.get('kobo_access_token'),
        }
        if request.method == 'POST':
            form_id = request.POST['form_id']
            r = requests.get(
                "https://kc.kobotoolbox.org/api/v1/forms/%s/form.json" %
                form_id,
                headers=headers)
            r.raise_for_status()
            form = r.json()
            survey = Survey(
                name=form['title'],
                cycle=Cycle.objects.get(pk=request.POST['cycle']),
                type=SurveyType.objects.get(pk=request.POST['survey_type']),
                form=r.text)
            survey.save()
            survey_kobo_project = SurveyKoboProject(
                survey=survey, form_id=form_id)
            survey_kobo_project.save()
            return redirect('/admin/umibukela/survey/%d' % survey.id)
        else:
            r = requests.get(
                "https://kc.kobotoolbox.org/api/v1/forms", headers=headers)
            r.raise_for_status()
            available_surveys = []
            for survey in r.json():
                if not SurveyKoboProject.objects.filter(
                        form_id=survey['formid']).count():
                    available_surveys.append(survey)
            return render(
                request, 'survey_from_kobo.html', {
                    'forms': available_surveys,
                    'cycles': Cycle.objects.all(),
                    'survey_types': SurveyType.objects.all(),
                })


def survey_kobo_submissions(request, survey_id):
    if not is_kobo_authed(request):
        return start_kobo_oauth(request)
    else:
        headers = {
            'Authorization':
            "Bearer %s" % request.session.get('kobo_access_token'),
        }
        survey = get_object_or_404(Survey, id=survey_id)
        form_id = survey.surveykoboproject.form_id
        r = requests.get(
            "https://kc.kobotoolbox.org/api/v1/data/%s" % form_id,
            headers=headers)
        r.raise_for_status()
        submissions = r.json()
        facilities = []
        facility_labels = {}
        form = survey.form
        if form.get_by_path('facility'):
            facility_q_name = 'facility'
        elif form.get_by_path('site'):
            facility_q_name = 'site'
        else:
            raise Exception('No facility/site/location question')
        for q in survey.form['children']:
            if q['name'] == facility_q_name:
                for o in q['children']:
                    facility_labels[o['name']] = o['label']
        facility_key = lambda r: r[facility_q_name]
        facility_sorted = sorted(submissions, key=facility_key, reverse=True)
        facilities = []
        for facility_name, facility_group in groupby(facility_sorted,
                                                     facility_key):
            facilities.append({
                'name': facility_name,
                'label': facility_labels[facility_name],
                'count': len(list(facility_group)),
            })
        crs_form = CRSFromKoboForm(facilities=facilities)
        if request.method == 'POST':
            num_facilities = request.POST['num_facilities']
            facility_crs = {}
            for i in xrange(int(num_facilities)):
                facility_name = request.POST['facility_%d' % i]
                crs_id = int(request.POST['crs_%d' % i])
                facility_crs[facility_name] = CycleResultSet.objects.get(
                    pk=crs_id)
            submissions = field_per_SATA_option(survey.form, submissions)
            submissions = skipped_as_na(survey.form, submissions)
            for answers in submissions:
                facility_name = answers[facility_q_name]
                submission = Submission(
                    answers=answers,
                    cycle_result_set=facility_crs[facility_name])
                submission.save()
            return HttpResponseRedirect(
                '/admin/umibukela/cycleresultset', status=303)
        return render(
            request, 'survey_kobo_submissions.html', {
                'submissions': submissions,
                'survey': survey,
                'facilities': facilities,
                'crs_form': crs_form,
            })


def kobo_forms(request):
    if not is_kobo_authed(request):
        return start_kobo_oauth(request)
    else:
        headers = {
            'Authorization':
            "Bearer %s" % request.session.get('kobo_access_token'),
        }
        r = requests.get(
            "https://kc.kobotoolbox.org/api/v1/forms", headers=headers)
        r.raise_for_status()
        available_surveys = r.json()
        surveys = []
        for survey_json in available_surveys:
            survey = {
                'title': survey_json['title'],
                'num_of_submissions': survey_json['num_of_submissions'],
            }
            if 'formid' in survey_json:
                survey['kobo_form_id'] = survey_json['formid']
                r = requests.get(
                    "https://kc.kobotoolbox.org/api/v1/forms/%d/form.json" %
                    survey_json['formid'],
                    headers=headers)
                r.raise_for_status()
                form = r.json()
                fields = form.get('children', [])
                facility_fields = [
                    c for c in fields
                    if c.get('name', None) in ('facility', 'site')
                ]
                if facility_fields:
                    survey['facilities'] = facility_fields[0]['children']
            surveys.append(survey)

        return render(request, 'kobo_forms.html', {
            'forms': surveys,
        })


def kobo_form_site_preview(request, kobo_form_id, site_name):
    if not is_kobo_authed(request):
        return start_kobo_oauth(request)
    else:
        headers = {
            'Authorization':
            "Bearer %s" % request.session.get('kobo_access_token'),
        }
        r = requests.get(
            "https://kc.kobotoolbox.org/api/v1/forms/%s/form.json" %
            kobo_form_id,
            headers=headers)
        r.raise_for_status()
        form = r.json()
        r = requests.get(
            "https://kc.kobotoolbox.org/api/v1/data/%s" % kobo_form_id,
            headers=headers)
        r.raise_for_status()
        submissions = r.json()
        responses = [
            s for s in submissions
            if s.get('facility', s.get('site', None)) == site_name
        ]
        responses = field_per_SATA_option(form, responses)
        map_questions(form, responses)

        if responses:
            df = pandas.DataFrame(responses)
            site_totals = analysis.count_submissions(df)
            site_results = analysis.count_options(df, form['children'])
            site_results = analysis.calc_q_percents(site_results)
            prev_results = None
            analysis.combine_curr_hist(site_results, prev_results)
        else:
            site_totals = {'male': 0, 'female': 0, 'total': 0}
            site_results = None

        for q in form['children']:
            for option in q.get('children', []):
                if option['name'] == site_name:
                    site_label = option['label']
        return render(
            request, 'survey_preview.html', {
                'site_name': site_label,
                'form_title': form['title'],
                'results': {
                    'questions_dict': site_results,
                    'totals': site_totals,
                }
            })


def is_kobo_authed(request):
    kobo_expiry = request.session.get('kobo_access_token_expiry', None)
    return kobo_expiry and kobo_expiry > datetime.utcnow().isoformat()


def start_kobo_oauth(request):
    refresh_token_query = UserKoboRefreshToken.objects.filter(pk=request.user)
    if refresh_token_query.count():
        refresh_token = refresh_token_query.get()
        kobo = Kobo.from_refresh_token(refresh_token.token)
        request.session['kobo_access_token'] = kobo.access_token
        request.session[
            'kobo_access_token_expiry'] = kobo.expiry_datetime.isoformat()
        refresh_token.token = kobo.refresh_token
        refresh_token.save()
        return redirect(request.path)
    else:
        state = {
            'path': request.path,
            'type': 'user',
        }
        return redirect(
            "https://kc.kobotoolbox.org/o/authorize?client_id=%s&response_type=code&scope=read&state=%s"
            % (settings.KOBO_CLIENT_ID, json.dumps(state)))


def programme_kobo_grant(request, programme_id):
    state = {
        'path': reverse(
            'admin:umibukela_programme_change', args=[programme_id]),
        'type': 'programme',
        'id': programme_id,
    }
    return redirect(
        "https://kc.kobotoolbox.org/o/authorize?client_id=%s&response_type=code&scope=read&state=%s"
        % (settings.KOBO_CLIENT_ID, json.dumps(state)))


def kobo_oauth_return(request):
    state = json.loads(request.GET.get('state'))
    redirect_uri = request.build_absolute_uri('/admin/kobo-oauth')
    kobo = Kobo.from_auth_code(request.GET.get('code'), redirect_uri)
    request.session['kobo_access_token'] = kobo.access_token
    request.session[
        'kobo_access_token_expiry'] = kobo.expiry_datetime.isoformat()
    if state['type'] == 'user':
        refresh_token, created = UserKoboRefreshToken.objects.get_or_create(
            user=request.user)
    elif state['type'] == 'programme':
        programme = Programme.objects.get(id=state['id'])
        refresh_token, created = ProgrammeKoboRefreshToken.objects.get_or_create(
            programme=programme)
    refresh_token.token = kobo.refresh_token
    refresh_token.save()
    return redirect(state['path'])


def province_summary_pdf(request, province_slug, survey_type_slug, cycle_id):
    province = get_object_or_404(Province, slug=province_slug)
    survey_type = get_object_or_404(SurveyType, slug=survey_type_slug)
    cycle = get_object_or_404(Cycle, id=cycle_id)
    # render poster as pdf
    url = reverse(
        'province-summary',
        kwargs={
            'province_slug': province_slug,
            'survey_type_slug': survey_type_slug,
            'cycle_id': cycle_id,
        })
    url = request.build_absolute_uri(url)
    pdf = wkhtmltopdf(
        url, **{
            'margin-top': '0.5cm',
            'margin-right': '0.5cm',
            'margin-bottom': '0.5cm',
            'margin-left': '0.5cm',
        })
    filename = (u'Summary for %s - %s - %s.pdf' %
                (province.name, survey_type.name, cycle.name)).encode(
                    'ascii', 'ignore')
    return PDFResponse(pdf, filename=filename, show_content_in_browser=True)


def province_summary(request, province_slug, survey_type_slug, cycle_id):
    province = get_object_or_404(Province, slug=province_slug)
    survey_type = get_object_or_404(SurveyType, slug=survey_type_slug)
    cycle = get_object_or_404(Cycle, id=cycle_id)

    result_sets = CycleResultSet.objects.filter(
        site__province=province, survey__cycle=cycle, survey__type=survey_type)

    form, gender_disagg, results, totals = analysis.cross_site_summary(
        result_sets)
    site_totals = totals.pop('per_site')
    for result_set in result_sets:
        result_set.totals = site_totals[result_set.site.id]

    return render(
        request, 'print-materials/location_cycle_summary.html', {
            'survey_type': survey_type,
            'ignore_paths': ['facility'],
            'ignore_types': IGNORE_TYPES,
            'multiple_choice_types': ['select all that apply', 'select one'],
            'form': form,
            'gender_disagg': gender_disagg,
            'location_name': province.name,
            'survey_type': survey_type,
            'cycle': cycle,
            'result_sets': result_sets,
            'results': {
                'questions_dict': results,
                'totals': totals,
            }
        })


def national_summary_pdf(request, survey_type_slug, cycle_id):
    survey_type = get_object_or_404(SurveyType, slug=survey_type_slug)
    cycle = get_object_or_404(Cycle, id=cycle_id)
    # render poster as pdf
    url = reverse(
        'national-summary',
        kwargs={
            'survey_type_slug': survey_type_slug,
            'cycle_id': cycle_id,
        })
    url = request.build_absolute_uri(url)
    pdf = wkhtmltopdf(
        url, **{
            'margin-top': '0.5cm',
            'margin-right': '0.5cm',
            'margin-bottom': '0.5cm',
            'margin-left': '0.5cm',
        })
    filename = (u'Summary for South Africa - %s - %s.pdf' %
                (survey_type.name, cycle.name)).encode('ascii', 'ignore')
    return PDFResponse(pdf, filename=filename, show_content_in_browser=True)


def national_summary(request, survey_type_slug, cycle_id):
    survey_type = get_object_or_404(SurveyType, slug=survey_type_slug)
    cycle = get_object_or_404(Cycle, id=cycle_id)

    result_sets = CycleResultSet.objects.filter(
        survey__cycle=cycle, survey__type=survey_type)

    form, gender_disagg, results, totals = analysis.cross_site_summary(
        result_sets)
    site_totals = totals.pop('per_site')
    for result_set in result_sets:
        result_set.totals = site_totals[result_set.site.id]

    return render(
        request, 'print-materials/location_cycle_summary.html', {
            'survey_type': survey_type,
            'ignore_paths': ['facility'],
            'ignore_types': IGNORE_TYPES,
            'multiple_choice_types': ['select all that apply', 'select one'],
            'form': form,
            'gender_disagg': gender_disagg,
            'location_name': 'South Africa',
            'survey_type': survey_type,
            'cycle': cycle,
            'result_sets': result_sets,
            'results': {
                'questions_dict': results,
                'totals': totals,
            }
        })


def national_poster_pdf(request, survey_type_slug, cycle_id):
    survey_type = get_object_or_404(SurveyType, slug=survey_type_slug)
    cycle = get_object_or_404(Cycle, id=cycle_id)
    # render poster as pdf
    url = reverse(
        'national-poster',
        kwargs={
            'survey_type_slug': survey_type_slug,
            'cycle_id': cycle_id,
        })
    url = request.build_absolute_uri(url)
    pdf = wkhtmltopdf(
        url, **{
            'margin-top': '0.5cm',
            'margin-right': '0.5cm',
            'margin-bottom': '0.5cm',
            'margin-left': '0.5cm',
        })
    filename = (u'Poster for South Africa - %s - %s.pdf' %
                (survey_type.name, cycle.name)).encode('ascii', 'ignore')
    return PDFResponse(pdf, filename=filename, show_content_in_browser=True)


def national_poster(request, survey_type_slug, cycle_id):
    survey_type = get_object_or_404(SurveyType, slug=survey_type_slug)
    cycle = get_object_or_404(Cycle, id=cycle_id)

    result_sets = CycleResultSet.objects.filter(
        survey__cycle=cycle, survey__type=survey_type)

    form, gender_disagg, results, curr_totals = analysis.cross_site_summary(
        result_sets)
    totals = {'current': curr_totals}

    return render(
        request, survey_type.poster_template, {
            'DEBUG':
            settings.DEBUG,
            'form':
            form,
            'layout_class':
            slugify(survey_type.name),
            'prev_date':
            None,
            'start_date':
            cycle.start_date,
            'end_date':
            cycle.end_date,
            'questions_dict':
            results,
            'sector':
            result_sets[0].site.sector.name,
            'location':
            'South Africa',
            'totals':
            totals,
            'funder_name':
            'MAVC',
            'survey_type':
            survey_type,
            'site_type':
            re.sub(TRIM_TYPE_RE, "", survey_type.name),
            'site_names':
            [re.sub(TRIM_SITE_RE, "", crs.site.name) for crs in result_sets],
        })


def province_poster_pdf(request, province_slug, survey_type_slug, cycle_id):
    province = get_object_or_404(Province, slug=province_slug)
    survey_type = get_object_or_404(SurveyType, slug=survey_type_slug)
    cycle = get_object_or_404(Cycle, id=cycle_id)
    # render poster as pdf
    url = reverse(
        'province-poster',
        kwargs={
            'province_slug': province_slug,
            'survey_type_slug': survey_type_slug,
            'cycle_id': cycle_id,
        })
    url = request.build_absolute_uri(url)
    pdf = wkhtmltopdf(
        url, **{
            'margin-top': '0.5cm',
            'margin-right': '0.5cm',
            'margin-bottom': '0.5cm',
            'margin-left': '0.5cm',
        })
    filename = (u'Poster for %s - %s - %s.pdf' %
                (province.name, survey_type.name, cycle.name)).encode(
                    'ascii', 'ignore')
    return PDFResponse(pdf, filename=filename, show_content_in_browser=True)


def province_poster(request, province_slug, survey_type_slug, cycle_id):
    province = get_object_or_404(Province, slug=province_slug)
    survey_type = get_object_or_404(SurveyType, slug=survey_type_slug)
    cycle = get_object_or_404(Cycle, id=cycle_id)

    result_sets = CycleResultSet.objects.filter(
        site__province=province, survey__cycle=cycle, survey__type=survey_type)

    form, gender_disagg, results, curr_totals = analysis.cross_site_summary(
        result_sets)
    totals = {'current': curr_totals}
    return render(
        request, survey_type.poster_template, {
            'DEBUG':
            settings.DEBUG,
            'form':
            form,
            'layout_class':
            slugify(survey_type.name),
            'prev_date':
            None,
            'start_date':
            cycle.start_date,
            'end_date':
            cycle.end_date,
            'questions_dict':
            results,
            'sector':
            result_sets[0].site.sector.name,
            'location':
            province.name,
            'totals':
            totals,
            'funder_name':
            'MAVC',
            'survey_type':
            survey_type,
            'site_type':
            re.sub(TRIM_TYPE_RE, "", survey_type.name),
            'site_names':
            [re.sub(TRIM_SITE_RE, "", crs.site.name) for crs in result_sets],
        })


def create_materials_zip(request, cycle_id):
    artifacts = []
    # We pre-generate the list of urls and directories to lean on
    # request.build_absolute_uri here, since we can only pass
    # serialisable variables to background_tasks.create_zip.
    cycle = Cycle.objects.get(id=cycle_id)
    for crs in CycleResultSet.objects.filter(survey__cycle=cycle):
        params = {'site_slug': crs.site.slug, 'result_id': crs.id}
        dir = os.path.join(
            crs.site.province.name.encode('ascii', 'ignore'),
            crs.partner.short_name.encode('ascii', 'ignore'),
            crs.site.name.encode('ascii', 'ignore'),
        )
        if 'citizen' in crs.survey.type.name.lower():
            url = request.build_absolute_uri(
                reverse('site-result-poster-pdf', kwargs=params))
            artifacts.append({
                'url': url,
                'dir': dir,
            })
            url = request.build_absolute_uri(
                reverse('site-result-handout-pdf', kwargs=params))
            artifacts.append({
                'url': url,
                'dir': dir,
            })
            url = request.build_absolute_uri(
                reverse('site-result-comments-pdf', kwargs=params))
            artifacts.append({
                'url': url,
                'dir': dir,
            })
        else:
            url = request.build_absolute_uri(
                reverse('site-result-summary-pdf', kwargs=params))
            artifacts.append({
                'url': url,
                'dir': dir,
            })
    Cycle.schedule_create_materials_zip(cycle_id, artifacts)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
