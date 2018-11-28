function fetch_period_results(short_name, cycle_id, date_string){
	 $.ajax({
	     url: '/programme/results/'+short_name+'/'+cycle_id,
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
