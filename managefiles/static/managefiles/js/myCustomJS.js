   // window.alert("It works");
var data = {'scans': {'VirusBuster': {'detected': true, 'version': '5.0.27.0', 'result': 'Trojan.VB.JFDE', 'update': '20100514'},
    'NOD32': {'detected': true, 'version': '5115', 'result': 'a variant of Win32/Qhost.NTY', 'update': '20100514'},
    'F-Prot': {'detected': false, 'version': '4.5.1.85', 'result': null, 'update': '20100514'},
    'Symantec': {'detected': true, 'version': '20101.1.0.89', 'result': 'Trojan.KillAV', 'update': '20100515'},
    'Norman': {'detected': true, 'version': '6.04.12', 'result': 'W32/Smalltroj.YFHZ', 'update': '20100514'},
    'TrendMicro-HouseCall': {'detected': true, 'version': '9.120.0.1004', 'result': 'TROJ_VB.JVJ', 'update': '20100515'},
    'Avast': {'detected': true, 'version': '4.8.1351.0', 'result': 'Win32:Malware-gen', 'update': '20100514'},
    'eSafe': {'detected': true, 'version': '7.0.17.0', 'result': 'Win32.TRVB.Acgy', 'update': '20100513'}
  }};
  var dataHtml = "";

  for (var i = 0; i < Object.keys(data.scans).length; i++) {
  		var antiVirus = data.scans[Object.keys(data.scans)[i]];
  		dataHtml = dataHtml + "<tr><td>" + Object.keys(data.scans)[i] + "</td>" +
  						"<td>" + antiVirus.detected + "</td>" +
						"<td>" + antiVirus.version + "</td>" +
						"<td>" + antiVirus.result + "</td>" +
						"<td>" + antiVirus.update + "</td>" +
					"</tr>";
	}
function header(report) {
  var htmlHeader = "<div class=\"row\"><div class=\"col-xs-12\"><div class=\"box\"><div class=\"box-header\">" +
				"<div class=\"box-name\"><!--i class=\"fa fa-usd\"></i--><span>Relatório " + report + "</span></div>" +
				"<div class=\"box-icons\"><a class=\"collapse-link\"><i class=\"fa fa-chevron-up\"></i></a>" +
					"<a class=\"expand-link\"><i class=\"fa fa-expand\"></i></a><a class=\"close-link\">" +
						"<i class=\"fa fa-times\"></i></a></div><div class=\"no-move\"></div></div>";

	return htmlHeader;
	}

  var htmlData = "<div class=\"box-content no-padding\">" +
  					"<table class=\"table table-bordered table-striped table-hover table-heading table-datatable\">" +
				"<thead>" +
						"<tr>" +
							"<th>Antivirus</th>" +
							"<th>Detectado</th>" +
							"<th>Versão</th>" +
							"<th>Resultado</th>" +
							"<th>Atualização</th>" +
						"</tr>" +
					"</thead>" +
					"<tbody>" +	dataHtml + "</tbody></table></div>";


  $(".virusTotalHtml").click(function(){
  	$(header("VirusTotal") + htmlData).appendTo("#virusTotal");
  	});

	console.log(dataHtml);
//$(dataHtml).appendTo("#virusTotal");
//window.alert(dataHtml);