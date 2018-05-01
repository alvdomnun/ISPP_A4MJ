function addChartIframeJS(idChart){

	$('#chart').empty();

	var htmlChart = '<div class="col-md-12" style="height="300">'+
						'<div class="row">'+
							'<div class="col-md-12">'+
								'<b><p style="text-align:center">chart id: '+idChart+'</p></b>'+
							'</div>'+	                    
		                    '<div class="col-md-12">'+
		                        '<canvas class="notebook-chart" id="'+idChart+'" width="auto" height="300"></canvas>'+
		                    '</div>'+
		                '</div>'+
	                '</div>';

	$('#chart').append(htmlChart);

	//Mostrar la gráfica con valores por defecto

	var ctx = document.getElementById(idChart);
	var myChart = new Chart(ctx, {
	    type: 'line',
	    data: {
	        labels: [],
	        datasets: [{
	            label: 'Nombre Gráfica',
	            data: [],
	            backgroundColor: [
	                'rgba(255, 99, 132, 0.2)',
	                'rgba(54, 162, 235, 0.2)',
	                'rgba(255, 206, 86, 0.2)',
	                'rgba(75, 192, 192, 0.2)',
	                'rgba(153, 102, 255, 0.2)',
	                'rgba(255, 159, 64, 0.2)'
	            ],
	            borderColor: [
	                'rgba(255,99,132,1)',
	                'rgba(54, 162, 235, 1)',
	                'rgba(255, 206, 86, 1)',
	                'rgba(75, 192, 192, 1)',
	                'rgba(153, 102, 255, 1)',
	                'rgba(255, 159, 64, 1)'
	            ],
	            borderWidth: 1
	        }]
	    },
	    options: {
	    	chartArea: {
		        backgroundColor: 'rgba(251, 255, 255, 0.4)',
		    },
	        maintainAspectRatio: false,
	        scales: {
	            yAxes: [{
	                ticks: {
	                    beginAtZero:true
	                }
	            }]
	        }
	    }
	});

}

function deleteChart(idChartRow,idRowPrincipalParameter,idBoxParameter,idColChartButtons){

	var element = $('#'+idChartRow);
	if(element != null){
		$('#'+idChartRow).remove();
	}

	$('#'+idColChartButtons+' button:last-child').remove();


	var htmlAddChartButton = 	'<button type="submit" class="btn btn-primary" onclick="addChart(\''+idRowPrincipalParameter+'\',\''+idBoxParameter+'\',\''+idColChartButtons+'\');">'+
                            		'Añadir Gráfica'+
                            	'</button>';

    $('#'+idColChartButtons).append(htmlAddChartButton);

}