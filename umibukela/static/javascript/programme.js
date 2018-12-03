function fetch_period_results(short_name, cycle_id, date_string){
    $('#period-name').html(date_string);
    $('#monitor-period-name').html(date_string);
    $('#community-period-name').html(date_string);
    fetch_submission_count(short_name, cycle_id, date_string);
    fetch_datastudio_results(short_name, cycle_id, date_string);
    fetch_community_results(short_name, cycle_id, date_string);
};

function fetch_submission_count(short_name, cycle_id,date_string){
    $.ajax({
	url: '/programme/submission/results/'+short_name+'/'+cycle_id,
	type: 'GET',
	success: function(data){
	    $('#submission_count').html(data.submission_count + ' total citzens surveyed');
	}
	
    });
}

function fetch_datastudio_results(short_name, cycle_id, date_string){
    $.ajax({
	     url: '/programme/datastudio/results/'+short_name+'/'+cycle_id,
	     type: 'GET',
	     success: function(data){
		 if (data){
		     $('#monitor-period-name').html(date_string);
		     var div_parent = document.createElement('div');
		     div_parent.className = 'row';
		     if (Object.keys(data.datastudio).length > 0){
			 for (survey_type in data.datastudio){
			     var div_child = document.createElement('div');
			     div_child.className='col-md-12 col-sm-12';
			     var survey_type_name = document.createTextNode(survey_type + 'Results Dashboard');
			     var h3 = document.createElement('h3');
			     h3.className='text-center';
			     h3.appendChild(survey_type_name);
			     var embed_div = document.createElement('div');
			     embed_div.className='embed-responsive embed-responsive-16by9';
			     var iframe = document.createElement('iframe');
			     iframe.setAttribute('width','auto');
			     iframe.setAttribute('height','450');
			     iframe.setAttribute('src',data.datastudio[survey_type]);
			     iframe.setAttribute('framework', '0');
			     iframe.setAttribute('style','border:0');
			     embed_div.appendChild(iframe);
			     div_child.appendChild(h3);
			     div_child.appendChild(embed_div);
			     div_parent.appendChild(div_child);
			     
			 }
			 $('#append-datastudio').empty();
			 var append_studio = document.getElementById('append-datastudio');
			 append_studio.appendChild(div_parent);
		     }else {
			 console.log("There is no survey results");
			 var no_result_text = document.createTextNode("No Results for this monitoring period");
			 var h3 = document.createElement('h3');
			 h3.className='text-center';
			 h3.appendChild(no_result_text);
			 
			 div_parent.appendChild(h3);
			 $('#append-datastudio').empty();
			 
			 var append_studio = document.getElementById('append-datastudio');
			 append_studio.appendChild(div_parent);
		     }
		     
		 }else{
		     console.log("No data here");
		 }
	     },
	     error: function(data){}
	     
	 });
};
function fetch_community_results(short_name, cycle_id, date_string){
	 $.ajax({
	     url: '/programme/community/results/'+short_name+'/'+cycle_id,
	     type: 'GET',
	     success: function(data){
		 if (data){
		     $('#community-period-name').html(date_string);
		     var tbody = document.getElementById('community-body');
		     if (Object.keys(data.partners).length > 0){
			 $('#community-body').empty();
			 for (p in data.partners){
			     console.log(data.partners[p].name);
			     var table_row = document.createElement('tr');
			     var row_name = document.createElement('td');
			     row_name.innerHTML = data.partners[p].name;
			     
			     var row_url = document.createElement('td');
			     var url = document.createElement('a');
			     url.setAttribute('href', data.partners[p].url);
			     url.innerHTML = 'View';
			     row_url.appendChild(url);
			     
			     var row_site = document.createElement('td');
			     row_site.innerHTML = data.partners[p].site;
			     var row_total = document.createElement('td');
			     row_total.innerHTML = data.partners[p].total;
			     table_row.appendChild(row_name);
			     table_row.appendChild(row_url);
			     table_row.appendChild(row_site);
			     table_row.appendChild(row_total);
			     tbody.appendChild(table_row);
			 }
			 
			 
		     }else {
			 console.log("There are no community results for this period");
			 $('#community-table').empty();
			 var h3 = document.createElement('h3');
			 h3.className='text-center';
			 h3.appendChild("No Results for this period");
			 var community_table = document.getElementById('community-table');
			 community_table.appendChild(h3);
			 
			 
		     }
		     
		 }else{
		     console.log("No data here");
		 }
	     },
	     error: function(data){}
	     
	 });
    
}
