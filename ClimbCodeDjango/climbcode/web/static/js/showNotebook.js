//Variables para generar ids unicos
var numBox = 0;
var numImg = 0;
var maxOrder = 0;
//Variable global seteada
var numParam = 0;

//Constante para recuperar parámetro para el Iframe
var ID_HIDDEN_NAME_PARAM = "input_hidden_parameter_id_name_param_";

function addNewTextBox(idNotebookContent,idNotebookBD){
	addTextBox(idNotebookContent,idNotebookBD,null,null,'');
}

function addTextBox(idNotebookContent,idNotebookBD,order,idBoxBD,content){

	var vistaEdicion = true;

	numBox++;
	var idBox = "idBox"+numBox;
	var idBoxParameter = "'idBox"+numBox+"'";
	var idFormBox = "form_box_"+idBox;
	var idFormBoxSubmitButton = "form_box_submit_button_"+idBox;
	var idInputText = "input_text_box_"+idBox;
	var idHiddenIdNotebook = "input_hidden_id_notebook_"+idBox;
	var idHiddenOrder = "input_hidden_order_"+idBox;
	var idHiddenIdBox = "input_hidden_id_box_"+idBox;
	if(order==null){
		maxOrder++;
		var order = maxOrder;
	}

	//Contar número de saltos de línea en content
	var numSaltos = content.split(/\r\n|\r|\n/).length;

	//HTML DE LA CAJA DE TEXTO
	var htmlTextBox = 	'<div class="col-md-10 custom-mt-1 offset-md-1" id="'+idBox+'">'+
							'<div class="row">'+
								'<div class="col-md-12 custom-mt-1" >'+
									'<div class="form-group" style="padding:12px;">'+
										'<textarea id="'+idInputText+'" class="form-control text-box-textarea" placeholder="Escribe aquí" disabled="disabled" style="background-color: white;">'+content+'</textarea>'+
           							'</div>'+
								'</div>'+
							'</div>'+
						'</div>';

    $('#'+idNotebookContent).append(htmlTextBox);

    for(i=0;i<numSaltos;i++){
    	var element = $('#'+idInputText);
    	auto_grow(element[0]);
    }

    // Comportamiento al pulsar GUARDAR -> Llamada Ajax

    $('#'+idFormBox).on('submit', function(event){
        event.preventDefault();
        console.log("form submitted!");
        //MANDAR COMO PARÁMETRO TODO INPUT QUE SEA NECESARIO RECUPERAR EN EL MÉTODO
        createUpdateTextBox(idHiddenIdNotebook,idHiddenOrder,idInputText,idHiddenIdBox);
    });


}

function auto_grow(element) {
    element.style.height = "5px";
    element.style.height = (element.scrollHeight)+"px";
}

function addNewCodeBox(idNotebookContent,idNotebookBD){
	return addCodeBox(idNotebookContent,idNotebookBD,null,null,'');
}

function addCodeBox(idNotebookContent,idNotebookBD,order,idBoxBD,content,idChart){

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
	//Add Parameter Button id
	var idAddParamButton = "id_add_parameter_button_"+numBox;
	var idAddParamButtonParameter = "'id_add_parameter_button_"+numBox+"'";	
	//Div Row Principal del contenido para concatenar la gráfica
	var idAddGraphicButton = "id_add_graphic_button_"+numBox;
	var idRowPrincipal = "id_code_box_row_"+idBox;
	var idRowPrincipalParameter = "'id_code_box_row_"+idBox+"'";
	//Div Col Add Delete Button Chart
	var idColChartButtons = "id_col_chart_buttons_"+idBox;
	var idColChartButtonsParameter = "'id_col_chart_buttons_"+idBox+"'";

	//ID IFRAME
	var idIframe = "id_iframe_code_box_"+numBox;

	//ID INPUT RESULTADO CODIGO
	var idInputResultado = 'resultado_'+idEditor;

	/* IDS FORM */
	var idFormBox = "form_box_"+idBox;
	var idFormBoxSubmitButton = "form_box_submit_button_"+idBox;
	var idHiddenIdNotebook = "input_hidden_id_notebook_"+idBox;
	var idHiddenOrder = "input_hidden_order_"+idBox;
	var idHiddenIdBox = "input_hidden_id_box_"+idBox;
	if(order==null){
		maxOrder++;
		var order = maxOrder;
	}

	if(content==''||content==null){
		content='//Escribe tu ejercicio con JavaScript\n'+
		'function saludo(){\n'+
		'	return "Hola Mundo";\n'+
		'}\n'+
		'\n'+
		'saludo();\n';
	}

	//HTML DE LA CAJA DE CÓDIGO

	var htmlCodeBox = 	'<div class="col-md-12 custom-mt-1" >'+
							'<div class="row" id="'+idBox+'">'+
	                            '<div class="col-md-10 custom-mt-1 offset-md-1" >'+
	                                '<div style="background-color: #ebebeb;margin-left: 30px; margin-right: 30px;width: auto;height: auto">'+
	                                    '<div class="row" id="'+idRowPrincipal+'">'+
	                                    	'<textarea id="'+idEditor+'" class="form-control text-box-textarea" placeholder="Escribe aquí" disabled="disabled" style="display:none;">'+content+'</textarea>'+
	                                        '<div class="col-md-12" style="margin-top: 20px;">'+	                                        
	                                                '<div class="row" style="padding: 15px;">'+                                                	
	                                                    '<div class="col-md-12 div-notebook-parameter" style="margin-top: 20px;background-color: white">'+
	                                                    '<h3 style="text-align:center">Parámetros</h3>'+
	                                                        '<div class="row" id="'+idDivParam+'">'+                                                          
	                                                            '<div id="'+idDivParamButton+'" class="col-md-2" style="margin-top: 20px;">'+                                                               
	                                                            '</div>'+
	                                                        '</div>'+
	                                                    '</div>'+
	                                                '</div>'+
	                                        '</div>'+
	                                        '<div id="'+idColChartButtons+'" class="col-md-4" style="margin-top: 20px;">'+
	                                            '<button type="submit" class="btn btn-primary" onclick="evalUserCodeAceIframe('+idEditorParameter+',\''+idDivParam+'\',\''+idIframe+'\',\''+idInputResultado+'\');">'+
	                                               'Ejecutar>>'+
	                                            '</button>'+
	                                            '<br><br>'+
	                                            '<h4>Resultado del código</h4>'+
	                                            '<input name="resultado_'+idEditor+'" class="form-control resultado_code_editor"  id="resultado_'+idEditor+'" type="text" disabled="disabled">'+
	                                            '<br><br>'+
	                                        '</div>'+
											'<div class="col-md-12" style="margin-top: 20px;">'+
	                                        	'<iframe style="width:100%;height: 0px;display:none" sandbox=\'allow-scripts\' id="'+idIframe+'" src="iframe_notebook"></iframe>'+
	                                        '</div>'+
	                                    '</div>'+

	                                '</div>'+
	                            '</div>'+
	                        '</div>'+
                        '</div>';

	$('#'+idNotebookContent).append(htmlCodeBox);

    if(idChart!=null && idChart!=''){
        setTimeout(
          function()
          {
            addChartIframe(idIframe,idBoxParameter,idColChartButtons,idChart,idAddGraphicButton,idBox);
          }, 3500);
    }

    if(idChart!=null && idChart!=''){
        setTimeout(
          function()
          {
            evalUserCodeAceIframe(idEditorParameter,idDivParam,idIframe,idInputResultado);
          }, 1500);
    }

    //Se devuelven los IDs de los divs necesarios para mostrar los parámetros
    var respuesta = [idDivParam,idDivParamButton];
    return respuesta;

}

function addCodeBoxPreviewNotebook(idNotebookContent,idNotebookBD,order,idBoxBD,content,idChart){

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
	//Add Parameter Button id
	var idAddParamButton = "id_add_parameter_button_"+numBox;
	var idAddParamButtonParameter = "'id_add_parameter_button_"+numBox+"'";
	//Div Row Principal del contenido para concatenar la gráfica
	var idAddGraphicButton = "id_add_graphic_button_"+numBox;
	var idRowPrincipal = "id_code_box_row_"+idBox;
	var idRowPrincipalParameter = "'id_code_box_row_"+idBox+"'";
	//Div Col Add Delete Button Chart
	var idColChartButtons = "id_col_chart_buttons_"+idBox;
	var idColChartButtonsParameter = "'id_col_chart_buttons_"+idBox+"'";

	//ID IFRAME
	var idIframe = "id_iframe_code_box_"+numBox;

	//ID INPUT RESULTADO CODIGO
	var idInputResultado = 'resultado_'+idEditor;

	/* IDS FORM */
	var idFormBox = "form_box_"+idBox;
	var idFormBoxSubmitButton = "form_box_submit_button_"+idBox;
	var idHiddenIdNotebook = "input_hidden_id_notebook_"+idBox;
	var idHiddenOrder = "input_hidden_order_"+idBox;
	var idHiddenIdBox = "input_hidden_id_box_"+idBox;
	if(order==null){
		maxOrder++;
		var order = maxOrder;
	}

	if(content==''||content==null){
		content='//Escribe tu ejercicio con JavaScript\n'+
		'function saludo(){\n'+
		'	return "Hola Mundo";\n'+
		'}\n'+
		'\n'+
		'saludo();\n';
	}

	//HTML DE LA CAJA DE CÓDIGO

	var htmlCodeBox = 	'<div class="col-md-12 custom-mt-1" >'+
							'<div class="row" id="'+idBox+'">'+
	                            '<div class="col-md-10 custom-mt-1 offset-md-1" >'+
	                                '<div style="background-color: #ebebeb;margin-left: 30px; margin-right: 30px;width: auto;height: auto">'+
	                                    '<div class="row" id="'+idRowPrincipal+'">'+
	                                    	'<textarea id="'+idEditor+'" class="form-control text-box-textarea" placeholder="Escribe aquí" disabled="disabled" style="display:none;">'+content+'</textarea>'+
	                                        '<div class="col-md-12" style="margin-top: 20px;">'+
	                                                '<div class="row" style="padding: 15px;">'+
	                                                    '<div class="col-md-12 div-notebook-parameter" style="margin-top: 20px;background-color: white">'+
	                                                    '<h3 style="text-align:center">Parámetros</h3>'+
	                                                        '<div class="row" id="'+idDivParam+'">'+
	                                                            '<div id="'+idDivParamButton+'" class="col-md-2" style="margin-top: 20px;">'+
	                                                            '</div>'+
	                                                        '</div>'+
	                                                    '</div>'+
	                                                '</div>'+
	                                        '</div>'+
	                                        '<div id="'+idColChartButtons+'" class="col-md-4" style="margin-top: 20px;">'+
	                                            '<button type="submit" class="btn btn-primary" onclick="evalUserCodeAceIframe('+idEditorParameter+',\''+idDivParam+'\',\''+idIframe+'\',\''+idInputResultado+'\');">'+
	                                               'Ejecutar>>'+
	                                            '</button>'+
	                                            '<br><br>'+
	                                            '<h4>Resultado del código</h4>'+
	                                            '<input name="resultado_'+idEditor+'" class="form-control resultado_code_editor"  id="resultado_'+idEditor+'" type="text" disabled="disabled">'+
	                                            '<br><br>'+
	                                        '</div>'+
											'<div class="col-md-12" style="margin-top: 20px;">'+
	                                        	'<iframe style="width:100%;height: 0px;display:none" sandbox=\'allow-scripts\' id="'+idIframe+'" src="iframe_notebook"></iframe>'+
	                                        '</div>'+
	                                    '</div>'+

	                                '</div>'+
	                            '</div>'+
	                        '</div>'+
                        '</div>';

	$('#'+idNotebookContent).append(htmlCodeBox);

    if(idChart!=null && idChart!=''){
        setTimeout(
          function()
          {
            addChartIframe(idIframe,idBoxParameter,idColChartButtons,idChart,idAddGraphicButton,idBox);
          }, 3500);
    }


    //Se devuelven los IDs de los divs necesarios para mostrar los parámetros
    var respuesta = [idDivParam,idDivParamButton,idEditor,idIframe,idInputResultado];
    return respuesta;

}

function addNewImageBox(idNotebookContent,idNotebookBD){
	addImageBox(idNotebookContent,idNotebookBD,null,null,'');
}

function addImageBox(idNotebookContent,idNotebookBD,order,idBoxBD,url){
	numBox++;
	//Box id
	var idBox = "idBox"+numBox;

	//Img id
	var idImg = "idImg"+idBox;
	//Input URL id
	var idUrlInput = "input_url_img_"+idBox;

	var idFormBox = "form_box_"+idBox;
	var idFormBoxSubmitButton = "form_box_submit_button_"+idBox;
	var idHiddenIdBox = "input_hidden_id_box_"+idBox;
	var idHiddenIdNotebook = "input_hidden_id_notebook_"+idBox;
	var idHiddenOrder = "input_hidden_order_"+idBox;

	if(order==null){
		maxOrder++;
		var order = maxOrder;
	}
    var urlImg = '/static/img/placeholder.png'
	if(url==null || url==""){
		url = '';
	}else{
	    urlImg = url;
	}

	//HTML DE LA CAJA DE IMAGEN
	var htmlImageBox = '<div class="col-md-12 custom-mt-1" id="'+idBox+'">'+
							'<div class="row">'+
								'<div class="col-md-12 custom-mt-1" >'+
									'<div class="form-group" style="padding:12px;">'+
		                            	'<img class="notebook-img" id="'+idImg+'" src="'+urlImg+'" height="256px" style="max-width: 100%;" />'+
		                        	'</div>'+
		                        '</div>'+
							'</div>'+
						'</div>';

	$('#'+idNotebookContent).append(htmlImageBox);


}

function evalUserCodeAce(idEditor){
    var editor = ace.edit(idEditor);
    var s = editor.getValue();
    var resultado = eval(s);
    document.getElementById("resultado_"+idEditor).value = String(resultado);
}

function setParametersIframe(idDivParamsCodeBox, idIframe){
	//En primer lugar, se borran todos los parámetros anteriores del iframe

    resetParamsIframe(idIframe);

    var childrens = $("#"+idDivParamsCodeBox).children();

	for (index1 = 0; index1 < childrens.length; ++index1) {
		//Obtenemos los inputs del form de cada parámetro
    	var children = childrens[index1];
    	var idChildren = children.id;

    	//Recorremos los inputs buscando el id y el valor del parámetro
    	inputs = $("#"+idChildren+" :input");
    	if(inputs!=null){
    		var idParam = null;
	    	var paramValue = null;

	    	for (index2 = 0; index2 < inputs.length; ++index2) {
	    		input = inputs[index2];
	    		
	    		if (input.id && input.id.indexOf(ID_HIDDEN_NAME_PARAM) == 0) {
		        	//Encontrado el id del parámetro
		        	idParam = input.value;
		    	}


	    	}
	    	//Si se ha recuperado el id del parámetro, obtenemos el valor
	    	if(idParam!=null){
		    	paramValue = $('#'+idParam).val();
	    	}
	    	//Si se ha recuperado correctamente el id y valor del parámetro,
	    	//se crea en el iframe
	    	if(idParam!=null && paramValue!=null){
	    		editCreateParamIframe(idIframe, idParam, paramValue);
	    	}
	    }
	}
}

function evalUserCodeAceIframe(idTextArea, idDivParamsCodeBox, idIframe, idInputResultado){

	var code = document.getElementById(idTextArea).value;

    /*
    	Comprobamos si el código contiene operaciones no permitidas. Estas son:
    		alert(
    		ajax.
    		window.
    		location.
    		eval(
	*/

	var rexExp = new RegExp("(?:^|\W)(eval)|(alert)|(window.)|(location.)|(ajax)(?:$|\W)");
	var invalidCode = rexExp.test(code);



    /*
    	Recuperamos los valores actuales de los parámetros de la caja de código
		para mandarlos al iframe
    */
    if(!invalidCode){
	    setParametersIframe(idDivParamsCodeBox, idIframe);   

		//Una vez seteados los parámetros en el iframe, ejecutamos el código en él
		data = ['evalCode', code, idInputResultado];

		var sandboxedFrame = document.getElementById(idIframe);

	    sandboxedFrame.contentWindow.postMessage(data, '*');
	}else{
		alert("El código contiene funciones no permitidas. Estas son:\n alert, ajax, window, location y eval");
	}
}

function evalUserCodeAceIframePreviewNotebook(idTextArea, idDivParamsCodeBox, idIframe, idInputResultado){

    var code = document.getElementById(idTextArea).value;
    deleteElement(idTextArea);

    /*
    	Comprobamos si el código contiene operaciones no permitidas. Estas son:
    		alert(
    		ajax.
    		window.
    		location.
    		eval(
	*/
	code = code.replace("\n", "");
	code = code.replace("&quot;", "'");

	var rexExp = new RegExp("(?:^|\W)(eval)|(alert)|(window.)|(location.)|(ajax)(?:$|\W)");
	var invalidCode = rexExp.test(code);



    /*
    	Recuperamos los valores actuales de los parámetros de la caja de código
		para mandarlos al iframe
    */
    if(!invalidCode){
	    setParametersIframe(idDivParamsCodeBox, idIframe);

		//Una vez seteados los parámetros en el iframe, ejecutamos el código en él
		data = ['evalCode', code, idInputResultado];

		var sandboxedFrame = document.getElementById(idIframe);

	    sandboxedFrame.contentWindow.postMessage(data, '*');
	}else{
		alert("El código contiene funciones no permitidas. Estas son:\n alert, ajax, window, location y eval");
	}
}

function addNewParameter(idParameterDiv,idButtonParameter,idBox){
	addParameter(idParameterDiv,idButtonParameter,idBox,null,'',null,null);
}

function addParameter(idParameterDiv,idButtonParameter,idBox,idParam,paramValue,idNameValue,nameParam){

	var numParameter = 0;

	if(idNameValue!=null && idNameValue!='null'){
    	var numParamActualString = idNameValue.substring(5,idNameValue.length);
        //Pasar el num como String a Integer
        var numParamActual = parseInt(numParamActualString);
        numParameter = numParamActual;
	}else{
		numParameter = getNumParam();
		numParameter++;
		setNumParam(numParameter);
	}

	/* IDS FORM */
	var idFormParam = "form_param_"+numParameter;
	var idDivParam = "div_param_"+numParameter;
	var idHiddenIdBox = "input_hidden_parameter_id_box_"+numParameter;
	var idHiddenIdPkParam = "input_hidden_parameter_id_pk_param_"+numParameter;
	//El nombre del id para obtenerse por código
	//NO CAMBIAR EL VALOR DE ESTA VARIABLE
	var idHiddenIdNameParam = ID_HIDDEN_NAME_PARAM+numParameter;
	//El nombre del parámetro establecido por el usuario
	var idNameParam = "input__name_param_"+numParameter;
	var idValueParam = "input_parameter_value_"+numParameter;

	/* FIN IDS FORM */

	var idParameterDivParameter = "'"+idParameterDiv+"'";
	var idButtonParameterParameter = "'"+idButtonParameter+"'";
	var idFormBoxSubmitButton = "form_box_submit_button_parameter"+numParameter;

	var idUrlInputParameter = "'idUrlInput"+numImg+"'";

    $('#'+idButtonParameter).remove();
    //Campo usado por el programador, y del que recoger el valor para persistir
    var idNameParameter = '';
    if(idNameValue==null){
    	var idNameParameter = 'param'+numParameter;
	}
	else{
		idNameParameter = idNameValue;
	}

	if(nameParam==null){
		nameParam = '';
	}

    var htmlParameter 	= 	'<div id="'+idDivParam+'" class="col-xs-4 col-md-4" style="margin-top: 20px;">'+
	    						'<form method="POST" id="'+idFormParam+'">'+
									'<input type="hidden" id="'+idHiddenIdBox+'" value="'+idBox+'">'+
									'<input type="hidden" id="'+idHiddenIdPkParam+'" value="'+idParam+'">'+
									'<input type="hidden" id="'+idHiddenIdNameParam+'" value="'+idNameParameter+'">'+

								'<label for="'+idNameParam+'" class="control-label">Nombre</label>'+
    							'<input value="'+nameParam+'" name="'+idNameParam+'" class="form-control" id="'+idNameParam+'" type="text" disabled="disabled">'+
    							'<label for="'+idNameParameter+'" class="control-label">Valor</label>'+
    							'<input value="'+paramValue+'" name="'+idNameParameter+'" class="form-control" id="'+idNameParameter+'" type="text" required>'+
    							'<br>'+
    							'</form>'+
    						'</div>'

    $('#'+idParameterDiv).append(htmlParameter);

}

function addParameterPreview(idParameterDiv,idButtonParameter,idBox,idParam,paramValue,idNameValue,nameParam){

	var numParameter = 0;

	if(idNameValue!=null && idNameValue!='null'){
    	var numParamActualString = idNameValue.substring(5,idNameValue.length);
        //Pasar el num como String a Integer
        var numParamActual = parseInt(numParamActualString);
        numParameter = numParamActual;
	}else{
		numParameter = getNumParam();
		numParameter++;
		setNumParam(numParameter);
	}

	/* IDS FORM */
	var idFormParam = "form_param_"+numParameter;
	var idDivParam = "div_param_"+numParameter;
	var idHiddenIdBox = "input_hidden_parameter_id_box_"+numParameter;
	var idHiddenIdPkParam = "input_hidden_parameter_id_pk_param_"+numParameter;
	//El nombre del id para obtenerse por código
	//NO CAMBIAR EL VALOR DE ESTA VARIABLE
	var idHiddenIdNameParam = ID_HIDDEN_NAME_PARAM+numParameter;
	//El nombre del parámetro establecido por el usuario
	var idNameParam = "input__name_param_"+numParameter;
	var idValueParam = "input_parameter_value_"+numParameter;

	/* FIN IDS FORM */

	var idParameterDivParameter = "'"+idParameterDiv+"'";
	var idButtonParameterParameter = "'"+idButtonParameter+"'";
	var idFormBoxSubmitButton = "form_box_submit_button_parameter"+numParameter;

	var idUrlInputParameter = "'idUrlInput"+numImg+"'";

    $('#'+idButtonParameter).remove();
    //Campo usado por el programador, y del que recoger el valor para persistir
    var idNameParameter = '';
    if(idNameValue==null){
    	var idNameParameter = 'param'+numParameter;
	}
	else{
		idNameParameter = idNameValue;
	}

	if(nameParam==null){
		nameParam = '';
	}

    var htmlParameter 	= 	'<div id="'+idDivParam+'" class="col-xs-4 col-md-4" style="margin-top: 20px;">'+
	    						'<form method="POST" id="'+idFormParam+'">'+
									'<input type="hidden" id="'+idHiddenIdBox+'" value="'+idBox+'">'+
									'<input type="hidden" id="'+idHiddenIdPkParam+'" value="'+idParam+'">'+
									'<input type="hidden" id="'+idHiddenIdNameParam+'" value="'+idNameParameter+'">'+

								'<label for="'+idNameParam+'" class="control-label">Nombre</label>'+
    							'<input value="'+nameParam+'" name="'+idNameParam+'" class="form-control" id="'+idNameParam+'" type="text" disabled="disabled">'+
    							'<label for="'+idNameParameter+'" class="control-label">Valor</label>'+
    							'<input value="'+paramValue+'" name="'+idNameParameter+'" class="form-control" id="'+idNameParameter+'" type="text" disabled="disabled">'+
    							'<br>'+
    							'</form>'+
    						'</div>'

    $('#'+idParameterDiv).append(htmlParameter);

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
		                        '<canvas class="notebook-chart" id="'+idChart+'" width="auto" height="300"></canvas>'+
		                    '</div>'+
		                '</div>'+
	                '</div>';

	$('#'+idRowPrincipalParameter).append(htmlChart);

	//Botón eliminar gráfica

	//Quitamos previamente el botón de aceptar

	$('#'+idColChartButtons+' button:last-child').remove();


	var htmlDeleteChartButton = '<button type="submit" class="btn btn-primary" onclick="deleteChart(\''+idChartRow+'\',\''+idRowPrincipalParameter+'\',\''+idBoxParameter+'\',\''+idColChartButtons+'\');">'+
                                   'Eliminar Gráfica'+
                                '</button>';

    $('#'+idColChartButtons).append(htmlDeleteChartButton);

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

function addChartIframe(idIframe,idBoxParameter,idColChartButtons,idChart,idAddGraphicButton,idBox){

	//TODO LLAMAR AL IFRAME PARA CARGAR LA GRÁFICA

	var sandboxedFrame = document.getElementById(idIframe);
    data = ['addChart', idChart];

    sandboxedFrame.contentWindow.postMessage(data, '*');

	//Botón eliminar gráfica

	//Quitamos previamente el botón de aceptar

    //Aumentar el tamaño del iframe para mostrar la gráfica

    document.getElementById(idIframe).style.height = "365px"
    document.getElementById(idIframe).style.display = "block"
    document.getElementById(idIframe).style.marginBottom = "20px";

}

function editCreateParamIframe(idIframe, idParam, valueParam){
    var sandboxedFrame = document.getElementById(idIframe);
    data = ['editCreateParam', idParam, valueParam];

    sandboxedFrame.contentWindow.postMessage(data, '*');
  }


  function resetParamsIframe(idIframe){
    var sandboxedFrame = document.getElementById(idIframe);
    data = ['resetParams'];

    sandboxedFrame.contentWindow.postMessage(data, '*');
  }

  function deleteParamIframe(idIframe, idParam){
    var sandboxedFrame = document.getElementById(idIframe);
    data = ['deleteParam', idParam];

    sandboxedFrame.contentWindow.postMessage(data, '*');
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


function getMaxOrder(){
	return maxOrder;
}

function setMaxOrder(maxOrderParam){
	maxOrder = maxOrderParam;
}

function getNumParam(){
	return numParam;
}

function setNumParam(numParameter){
	numParam = numParameter;
}

function deleteElement(idElement){
	$('#'+idElement).remove();
}

// left: 37, up: 38, right: 39, down: 40,
// spacebar: 32, pageup: 33, pagedown: 34, end: 35, home: 36
var keys = {37: 1, 38: 1, 39: 1, 40: 1};

function preventDefault(e) {
  e = e || window.event;
  if (e.preventDefault)
      e.preventDefault();
  e.returnValue = false;  
}

function preventDefaultForScrollKeys(e) {
    if (keys[e.keyCode]) {
        preventDefault(e);
        return false;
    }
}

function disableScroll() {
  if (window.addEventListener) // older FF
      window.addEventListener('DOMMouseScroll', preventDefault, false);
  window.onwheel = preventDefault; // modern standard
  window.onmousewheel = document.onmousewheel = preventDefault; // older browsers, IE
  window.ontouchmove  = preventDefault; // mobile
  document.onkeydown  = preventDefaultForScrollKeys;
}

function enableScroll() {
    if (window.removeEventListener)
        window.removeEventListener('DOMMouseScroll', preventDefault, false);
    window.onmousewheel = document.onmousewheel = null; 
    window.onwheel = null; 
    window.ontouchmove = null;  
    document.onkeydown = null;  
}