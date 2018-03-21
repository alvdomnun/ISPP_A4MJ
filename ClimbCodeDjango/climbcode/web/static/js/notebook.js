//Variables para generar ids unicos
var numBox = 0;
var numImg = 0;
var numParameter = 0;

function prueba(){
	alert(saludo);
}


function addTextBox(idNotebookContent){
	numBox++;
	var idBox = "idBox"+numBox;
	var idBoxParameter = "'idBox"+numBox+"'";

	//HTML DE LA CAJA DE TEXTO
		var htmlTextBox = 	'<div class="col-md-10 custom-mt-1 offset-md-1" id="'+idBox+'">'+
								'<div class="row">'+
									'<div class="col-md-12 custom-mt-1" >'+
										'<div class="form-group" style="padding:12px;">'+
			                            	'<textarea onkeyup="auto_grow(this)" class="form-control text-box-textarea" placeholder="Write here"></textarea>'+
			                         		/*'<button class="btn btn-info pull-right" style="margin-top:10px" type="button">Save</button>'+*/
			                         		'<button class="btn btn-danger pull-right" style="margin-top:10px" onclick="deleteElement('+idBoxParameter+')" type="button">Delete</button>'+
			                        	'</div>'+
									'</div>'+
								'</div>'+
							'</div>';

    $('#'+idNotebookContent).append(htmlTextBox);

	$('.animated').autosize({append: "\n"});


}

function auto_grow(element) {
    element.style.height = "5px";
    element.style.height = (element.scrollHeight)+"px";
}

function addCodeBox(idNotebookContent){
	numBox++;
	var idBox = "idBox"+numBox;
	var idBoxParameter = "'idBox"+numBox+"'";

	//Editor id
	var idEditor = "idEditor"+numBox;
	var idEditorParameter = "'idEditor"+numBox+"'";
	//Div Parameter id
	var idDivParam = "id_div_parameter_"+numBox;
	var idDivParamParameter = "'id_div_parameter_"+numBox+"'";
	//Div Parameter Button id
	var idDivParamButton = "id_div_parameter_button_"+numBox;
	var idDivParamButtonParameter = "'id_div_parameter_button_"+numBox+"'";
	//Div Row Principal del contenido para concatenar la gráfica
	var idRowPrincipal = "id_code_box_row_"+idBox;
	var idRowPrincipalParameter = "'id_code_box_row_"+idBox+"'";
	//Div Col Add Delete Button Chart
	var idColChartButtons = "id_col_chart_buttons_"+idBox;
	var idColChartButtonsParameter = "'id_col_chart_buttons_"+idBox+"'";
	

	//HTML DE LA CAJA DE CÓDIGO

	var htmlCodeBox = 	'<div class="col-md-12 custom-mt-1" >'+
							'<div class="row" id="'+idBox+'">'+
	                            '<div class="col-md-10 custom-mt-1 offset-md-1" >'+
	                                '<h2 style="text-align: center">CODE BOX</h2>'+
	                                '<div style="background-color: #ebebeb;margin-left: 30px; margin-right: 30px;width: auto;height: auto">'+
	                                    '<div class="row" id="'+idRowPrincipal+'">'+
	                                        '<div class="col-md-12">'+
	                                            '<div id="'+idEditor+'">'+
	                                            '</div>'+
	                                        '</div>'+
	                                        
	                                        '<div class="col-md-12" style="margin-top: 20px;">'+
	                                        '<button class="btn btn-danger pull-right" style="margin-top:10px" onclick="deleteElement('+idBoxParameter+')" type="button">Delete</button>'+
	                                                '<div class="row">'+                                                	
	                                                    '<div class="col-md-12 div-notebook-parameter" style="margin-top: 20px;background-color: white">'+
	                                                    '<h3 style="text-align:center">Parameters</h3>'+
	                                                        '<div class="row" id="'+idDivParam+'">'+                                                          
	                                                            '<div id="'+idDivParamButton+'" class="col-md-2" style="margin-top: 20px;">'+
	                                                            	'<p>Add Parameter</p>'+
	                                                                '<button type="submit" class="btn btn-primary" onclick="addParameter('+idDivParamParameter+','+idDivParamButtonParameter+');">'+
	                                                                   'Add'+
	                                                                '</button>'+                                                                
	                                                            '</div>'+
	                                                        '</div>'+
	                                                    '</div>'+
	                                                '</div>'+
	                                        '</div>'+
	                                        '<div id="'+idColChartButtons+'" class="col-md-4" style="margin-top: 20px;">'+
	                                            '<button type="submit" class="btn btn-primary" onclick="evalUserCodeAce('+idEditorParameter+');">'+
	                                               'Run >>'+
	                                            '</button>'+
	                                            '<br><br>'+
	                                            '<h4>Code Result</h4>'+
	                                            '<input name="resultado_'+idEditor+'" class="form-control resultado_code_editor"  id="resultado_'+idEditor+'" type="text" disabled="disabled">'+
	                                            '<br><br>'+
	                                            '<button type="submit" class="btn btn-primary" onclick="addChart('+idRowPrincipalParameter+','+idBoxParameter+','+idColChartButtonsParameter+');">'+
	                                               'Add Chart'+
	                                            '</button>'+
	                                        '</div>'+
	                                    '</div>'+
	                                '</div>'+
	                            '</div>'+
	                        '</div>'+
                        '</div>';

	$('#'+idNotebookContent).append(htmlCodeBox);

	var editor = ace.edit(idEditor);
                editor.getSession().setMode("ace/mode/javascript");
                editor.getSession().setTabSize(4);
                editor.getSession().setUseWrapMode(true);
                editor.setFontSize(16);
                editor.setShowPrintMargin(false);
                var heightUpdateFunction = function() {                    
                    $('#'+idEditor).height("250px");
                    $('#editor-section').height("250px");
                    // This call is required for the editor to fix all of
                    // its inner structure for adapting to a change in size
                    editor.resize();
                    };
                // Set initial size to match initial content
                heightUpdateFunction();
                // Whenever a change happens inside the ACE editor, update
                // the size again
                editor.getSession().on('change', heightUpdateFunction);
}

function addImageBox(idNotebookContent){
	numBox++;
	//Box id
	var idBox = "idBox"+numBox;
	var idBoxParameter = "'idBox"+numBox+"'";

	//Img id
	numImg++;
	var idImg = "idImg"+numImg;
	var idImgParameter = "'idImg"+numImg+"'";
	//Input URL id
	var idUrlInput = "idUrlInput"+numImg;
	var idUrlInputParameter = "'idUrlInput"+numImg+"'";


	//HTML DE LA CAJA DE IMAGEN
	var htmlImageBox = '<div class="col-md-12 custom-mt-1" id="'+idBox+'">'+
							'<div class="row">'+
								'<div class="col-md-12 custom-mt-1" >'+
									'<div class="form-group" style="padding:12px;">'+
		                            	'<img class="notebook-img" id="'+idImg+'" src="" height="256px" width="256px" />'+		                         		
		                        	'</div>'+
		                        '</div>'+
		                        '<div class="col-md-6 offset-md-3" >'+
		                        		'<input class="form-control" id="'+idUrlInput+'" type="text" placeholder="Set URL">'+
								'</div>'+
								'<div class="col-md-12 offset-md-3" >'+
		                         		'<button class="btn btn-info pull-right" style="margin-top:10px" onclick="updateImg('+idImgParameter+','+idUrlInputParameter+')" type="button">Update URL</button>'+
		                         		'<button class="btn btn-danger pull-right" style="margin-top:10px" onclick="deleteElement('+idBoxParameter+')" type="button">Delete</button>'+
								'</div>'+

							'</div>'+
						'</div>';

	$('#'+idNotebookContent).append(htmlImageBox);
}

function deleteElement(idElement){
	console.log('hola');
	$('#'+idElement).remove();
}

function updateImg(idImgParameter,idUrlInputParameter){
	urlInputVal = document.getElementById(idUrlInputParameter).value;
	$("#"+idImgParameter).attr("src",urlInputVal);
}


function evalUserCodeAce(idEditor){
    var editor = ace.edit(idEditor);
    var s = editor.getValue();
    var resultado = eval(s);
    document.getElementById("resultado_"+idEditor).value = String(resultado);
}

function addParameter(idParameterDiv,idButtonParameter){

	numParameter++;

	var idParameterDivParameter = "'"+idParameterDiv+"'";
	var idButtonParameterParameter = "'"+idButtonParameter+"'";

	var idUrlInputParameter = "'idUrlInput"+numImg+"'";

    $('#'+idButtonParameter).remove();
    var idNextParameter = 'param'+numParameter;

    var htmlParameter 	= 	'<div class="col-md-2" style="margin-top: 20px;">'+
    							'<p>id: '+idNextParameter+'</p>'+
    							'<input name="'+idNextParameter+'" class="form-control" id="'+idNextParameter+'" type="text">'+
    						'</div>'

    $('#'+idParameterDiv).append(htmlParameter);

    var htmlButton		=	'<div id="'+idButtonParameter+'" class="col-md-2" style="margin-top: 20px;">'+
    							'<p>Add Parameter</p>'+
    							'<button type="submit" class="btn btn-primary" onclick="addParameter('+idParameterDivParameter+','+idButtonParameterParameter+');"> Add </button>'+
							'</div>'


    $('#'+idParameterDiv).append(htmlButton);
}

function addChart(idRowPrincipalParameter,idBoxParameter,idColChartButtons){

	var idChart = "myChart_"+idBoxParameter;

	var idChartRow = idChart+'_row';

	var element = $('#'+idChartRow);
	if(element != null){
		$('#'+idChartRow).remove();
	}

	var htmlChart = '<div class="col-md-12" id="'+idChartRow+'" style="height="300">'+
						'<div class="row">'+
							'<div class="col-md-12">'+
								'<b><p style="text-align:center">chart id: '+idChart+'</p></b>'+
							'</div>'+	                    
		                    '<div class="col-md-12">'+
		                        '<canvas id="'+idChart+'" width="auto" height="300"></canvas>'+
		                    '</div>'+
		                '</div>'+
	                '</div>';

	$('#'+idRowPrincipalParameter).append(htmlChart);

	//Botón eliminar gráfica

	//Quitamos previamente el botón de aceptar

	$('#'+idColChartButtons+' button:last-child').remove();


	var htmlDeleteChartButton = '<button type="submit" class="btn btn-primary" onclick="deleteChart(\''+idChartRow+'\',\''+idRowPrincipalParameter+'\',\''+idBoxParameter+'\',\''+idColChartButtons+'\');">'+
                                   'Delete Chart'+
                                '</button>';

    $('#'+idColChartButtons).append(htmlDeleteChartButton);

	//Mostrar la gráfica con valores por defecto

	var ctx = document.getElementById(idChart);
	var myChart = new Chart(ctx, {
	    type: 'line',
	    data: {
	        labels: [],
	        datasets: [{
	            label: 'Sample Chart',
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
                            		'Add Chart'+
                            	'</button>';

    $('#'+idColChartButtons).append(htmlAddChartButton);



}