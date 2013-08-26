$(function() {

    $('#dcm_tabs a:last').tab('show');

	//dynamically change type to object instead of an array
	dcm.study = dcm.study[0];

    dcm.invert = false;

	$("#study_gallery").html('something');
	$("#dcm_header").html('<h3>' + dcm.study.title + '</h3>');

	$("#dcmview_image").attr('src', dcm.study.directory + '/' + dcm.series[0].filename + '.png');

    //dcm.imageRender();

	var gal_content = '';

	for (var i = 0; i < dcm.series.length; i++) {

		gal_content += '<a href="/dcmview/' + dcm.study.id + '/series/' + dcm.series[i].id + '" series_ID="' + dcm.series[i].id + '" class="dcm_series">' + 
					   '	<img src="' + dcm.study.directory + '/' + dcm.series[i].filename + 
					   		'.png" style="width: 80px; height: 80px; margin: 2px;" />' + 
					   	'</a>';

	}

	$("#study_gallery").html(gal_content);

	$(".dcm_series").on("click", function(e) {

		e.preventDefault();

		var switch_img = $(this).find("img").attr("src");

        $("#dcmview_image").removeAttr("data-caman-id");

        Caman("#dcmview_image", switch_img, function() {

            dcm.getFilters(this);

            this.render();

        });

		//$("#dcmview_image").attr('src', switch_img);

         //dcm.imageRender();

		$.ajax({
			"url": "/dcmview/series/" + $(this).attr("series_ID"),
			"type": "POST",
			"dataType": "json",
			"success": function(res) {
				dcm.study = res.study;
				dcm.dicom = $.parseJSON(res.dcm);

				dcm.reloadTags();
			}
		});

	});

	dcm.reloadTags(true);

    $(".filter").on("keyup", function(e) {

        Caman("#dcmview_image", function() {
            
            var that = this;

            this.revert();

            dcm.getFilters(that);

            //this.contrast($("#contrast").val());
            //this.brightness($("#brightness").val());
            //this.exposure($("#exposure").val());
            //this.gamma($("#gamma").val());
            //this.hue($("#hue").val());
            //this.saturation($("#saturation").val());

            this.render();

        });

    });

    $("#invert").on("click", function() {

        if (dcm.invert)
            dcm.invert = false;
        else
            dcm.invert = true;

        Caman("#dcmview_image", function() {
            this.invert().render();
        });
    });

    $("#reset").on("click", function() {
        dcm.resetFilters();
    });

});

dcm.getFilters = function(context) {

    $(".filter").each(function() {

        var val = $(this).val();

        if (val == "" || (isNaN(val) && val.indexOf("-") == -1)) {
            val = 0;
            $(this).val("0");
        }

        context[$(this).attr("id")](val);

    });

    if (dcm.invert)
        context.invert();

};

dcm.resetFilters = function() {

    $(".filter").each(function() {

        if ($(this).attr("id") == "gamma")
            $(this).val("1");
        else
            $(this).val("0");

    });

    if (dcm.invert == true)
        dcm.invert = false;

    Caman("#dcmview_image", function() {
        this.revert();
        this.render();
    });

}

dcm.imageRender = function() {

    dcm.caman = Caman("#dcmview_image");
    console.log('imageRender');

}

dcm.reloadTags = function(first) {

    if (typeof first === "undefined")
        first = false;

	var tag_content = '<thead>' +
                        '<tr>' + 
                            '<th>Element</th>' + 
                            '<th>Value</th>' + 
                            '</tr>' + 
                      '</thead>' + 
                      '<tbody>';

	for (key in dcm.dicom) {

		if (dcm.dicom[key] !== "" || dcm.dicom[key] !== " ") {

			tag_content += '<tr>' + 
					  '	<td>' + key + '</td>' + 
					  '	<td>' + dcm.dicom[key].replace(/["']/g, "") + '</td>' + 
					  '</tr>';

		}

	}

    tag_content += '</tbody>';

    /*if (!first) {

        dcm.datatable.fnClearTable();
        $("#dcm").html(tag_content);
        dcm.datatable.fnDraw();

    } else {*/

        var options = {
            "sPaginationType": "bootstrap",
            "bDestroy": true
        };

        //dataTables initialization
        $("#dcm").html(tag_content);
        dcm.datatable = $("#dcm").dataTable(options);

    //}

};

/* API method to get paging information */
$.fn.dataTableExt.oApi.fnPagingInfo = function ( oSettings )
{
    return {
        "iStart":         oSettings._iDisplayStart,
        "iEnd":           oSettings.fnDisplayEnd(),
        "iLength":        oSettings._iDisplayLength,
        "iTotal":         oSettings.fnRecordsTotal(),
        "iFilteredTotal": oSettings.fnRecordsDisplay(),
        "iPage":          oSettings._iDisplayLength === -1 ?
            0 : Math.ceil( oSettings._iDisplayStart / oSettings._iDisplayLength ),
        "iTotalPages":    oSettings._iDisplayLength === -1 ?
            0 : Math.ceil( oSettings.fnRecordsDisplay() / oSettings._iDisplayLength )
    };
}
 
/* Bootstrap style pagination control */
$.extend( $.fn.dataTableExt.oPagination, {
    "bootstrap": {
        "fnInit": function( oSettings, nPaging, fnDraw ) {
            var oLang = oSettings.oLanguage.oPaginate;
            var fnClickHandler = function ( e ) {
                e.preventDefault();
                if ( oSettings.oApi._fnPageChange(oSettings, e.data.action) ) {
                    fnDraw( oSettings );
                }
            };
 
            $(nPaging).addClass('pagination').append(
                '<ul>'+
                    '<li class="prev disabled"><a href="#">&larr; '+oLang.sPrevious+'</a></li>'+
                    '<li class="next disabled"><a href="#">'+oLang.sNext+' &rarr; </a></li>'+
                '</ul>'
            );
            var els = $('a', nPaging);
            $(els[0]).bind( 'click.DT', { action: "previous" }, fnClickHandler );
            $(els[1]).bind( 'click.DT', { action: "next" }, fnClickHandler );
        },
 
        "fnUpdate": function ( oSettings, fnDraw ) {
            var iListLength = 5;
            var oPaging = oSettings.oInstance.fnPagingInfo();
            var an = oSettings.aanFeatures.p;
            var i, j, sClass, iStart, iEnd, iHalf=Math.floor(iListLength/2);
 
            if ( oPaging.iTotalPages < iListLength) {
                iStart = 1;
                iEnd = oPaging.iTotalPages;
            }
            else if ( oPaging.iPage <= iHalf ) {
                iStart = 1;
                iEnd = iListLength;
            } else if ( oPaging.iPage >= (oPaging.iTotalPages-iHalf) ) {
                iStart = oPaging.iTotalPages - iListLength + 1;
                iEnd = oPaging.iTotalPages;
            } else {
                iStart = oPaging.iPage - iHalf + 1;
                iEnd = iStart + iListLength - 1;
            }
 
            for ( i=0, iLen=an.length ; i<iLen ; i++ ) {
                // Remove the middle elements
                $('li:gt(0)', an[i]).filter(':not(:last)').remove();
 
                // Add the new list items and their event handlers
                for ( j=iStart ; j<=iEnd ; j++ ) {
                    sClass = (j==oPaging.iPage+1) ? 'class="active"' : '';
                    $('<li '+sClass+'><a href="#">'+j+'</a></li>')
                        .insertBefore( $('li:last', an[i])[0] )
                        .bind('click', function (e) {
                            e.preventDefault();
                            oSettings._iDisplayStart = (parseInt($('a', this).text(),10)-1) * oPaging.iLength;
                            fnDraw( oSettings );
                        } );
                }
 
                // Add / remove disabled classes from the static elements
                if ( oPaging.iPage === 0 ) {
                    $('li:first', an[i]).addClass('disabled');
                } else {
                    $('li:first', an[i]).removeClass('disabled');
                }
 
                if ( oPaging.iPage === oPaging.iTotalPages-1 || oPaging.iTotalPages === 0 ) {
                    $('li:last', an[i]).addClass('disabled');
                } else {
                    $('li:last', an[i]).removeClass('disabled');
                }
            }
        }
    }
} );
