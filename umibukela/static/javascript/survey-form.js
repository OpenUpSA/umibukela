django.jQuery(document).ready(function() {
  var $ = django.jQuery;



  var listProjects = function() {
    $.ajax('https://kc.kobotoolbox.org/api/v1/projects', {
      dataType: 'json',
      headers: {
        'Authorization': 'Token ' + kobo_access_token
      },
      crossDoamin: false,
      error: function(jqXHR, textStatus, errorThrown) {
        alert(textStatus + '\n' + errorThrown);
      },
      success: function(data, textStatus, jqXHR) {
        var container = $('#project-list-container');
        container.empty();
        var select = $('<select />');
        $.each(data, function(idx, project) {
          select.append('<option value="' + project.url + '">' + project.name + '</option>');
        });
      }
    });
  };

  if (kobo_authed) {
    $('.add-button').removeClass('disabled');
  } else {
    $('#kobo-import-container').append('<a href="https://kc.kobotoolbox.org/o/authorize?client_id=' + kobo_client_id + '&response_type=code&scope=read&state=' + path + '">Login to Kobo</a>');
  }

  $('.add-button').click(listProjects);
});
