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
	var htmlTextBox = 	'<div class="col-md-12 custom-mt-1" id="'+idBox+'">'+
							'<div class="row">'+
								'<div class="col-md-12 custom-mt-1" >'+
									'<div class="form-group" style="padding:12px;">'+
		                            	'<textarea class="form-control animated" placeholder="Write here"></textarea>'+
		                         		'<button class="btn btn-info pull-right" style="margin-top:10px" type="button">Save</button>'+
		                         		'<button class="btn btn-danger pull-right" style="margin-top:10px" onclick="deleteElement('+idBoxParameter+')" type="button">Delete</button>'+
		                        	'</div>'+
								'</div>'+
							'</div>'+
						'</div>';

    $('#'+idNotebookContent).append(htmlTextBox);

}

function addCodeBox(idNotebookContent){
	numBox++;
	var idBox = "idBox"+numBox;
	var idBoxParameter = "'idBox"+numBox+"'";

	//Editor id
	numImg++;
	var idEditor = "idEditor"+numBox;
	var idEditorParameter = "'idEditor"+numBox+"'";

	//HTML DE LA CAJA DE CÓDIGO

	var htmlCodeBox = 		'<div class="col-md-12 custom-mt-1" id="'+idBox+'">'+	
								'<div class="row">'+
								    '<div class="col-md-12 custom-mt-1" >'+
								    	'<h3 style="text-align: center">CODE BOX</h3>'+
								    	'<div style="background-color: white;margin-left: 30px; margin-right: 30px;width: auto">'+
									        '<div class="row">'+
									            '<div class="col-md-12">'+
									                '<div id="'+idEditor+'">alert(2);'+
									                '</div>'+
									            '</div>'+
									        '</div>'+
									        '<button class="btn btn-info pull-right" style="margin-top:10px" type="button">Save</button>'+
			                         		'<button class="btn btn-danger pull-right" style="margin-top:10px" onclick="deleteElement('+idBoxParameter+')" type="button">Delete</button>'+
									    '</div>'+
									'</div>'+
									'<div class="col-md-4" style="margin-top: 20px;">'+
                                        '<button type="submit" class="btn btn-primary" onclick="evalUserCodeAce('+idEditorParameter+');">'+
                                           'Run >>'+
                                        '</button>'+
                                        '<br><br>'+
                                        '<p> Resultado caja sintaxis: </p>'+
                                        '<input name="resultado_'+idEditor+'" class="form-control"  id="resultado_'+idEditor+'" type="text" disabled="disabled">'+
                                    '</div>'+
								'</div>'+
							'</div>';

	$('#'+idNotebookContent).append(htmlCodeBox);
	var editor = ace.edit(idEditor);
                editor.getSession().setMode("ace/mode/javascript");
                editor.getSession().setTabSize(4);
                editor.getSession().setUseWrapMode(true);
                editor.setShowPrintMargin(false);
                var heightUpdateFunction = function() {                    
                    $('#'+idEditor).height("200px");
                    $('#editor-section').height("200px");
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
		                        '<div class="col-md-6 col-md-offset-3" >'+
		                        		'<input class="form-control" id="'+idUrlInput+'" type="text" placeholder="Set URL">'+
								'</div>'+
								'<div class="col-md-12" >'+
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