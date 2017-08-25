let Coral = (() => {
	const _baseUrl = '/';
	let $_periodpicker = $(".periodpicker");
	let $_merchant = $("#merchant");
	let $_impression = $("#impression");
	let $_click = $("#click");
	let $_registration = $("#registration");
	let $_depo = $("#newDepo");
	let $_commission = $("#commission");

	const sendRequest = (endPoint, params, callback) => {
		$.ajax({
			url : _baseUrl + endPoint,
			data : JSON.stringify(params),
			contentType : "application/json",
			type : "POST",
			success : (response) => {
				if (!response.status) {
					alert(response.message);
					$_impression.text("");
					$_click.text("");
					$_registration.text("");
					$_depo.text("");
					$_commission.text("");
					$_merchant.text("");
				}
				else if (typeof callback === 'function') {
					callback(response.jsonData);
				}
			},
			error : (error) => {
				alert("Something went wrong....");
			},
		});
	}

	const periodpicker = (val) => {
		sendRequest("coral/", {"val" : val, "state" : "1"}, (results) => {
			let val = $_periodpicker.val();
			if (val == 1) {
				$_merchant.text(results[0].merchant);
				$_impression.text(results[0].impression);
				$_click.text(results[0].click);
				$_registration.text(results[0].registration);
				$_depo.text(results[0].new_deposit);
				$_commission.text("£ " + results[0].commission);
				$("#title").text("Quick Stats at a Glance | MTD");
				$("#datepicker").datepicker({ dateFormat: "m/d/Y", changeMonth: true,
            changeYear: true, yearRange: '1900:2020', defaultDate: ''}).val("");
			}
			else if (val == 2) {
				$_merchant.text(results[0].merchant);
				$_impression.text(results[0].impreytd);
				$_click.text(results[0].cliytd);
				$_registration.text(results[0].regytd);
				$_depo.text(results[0].ndytd);
				$_commission.text("£ " + results[0].commiytd);
				$("#title").text("Quick Stats at a Glance | YTD");
				$("#datepicker").datepicker({ dateFormat: "m/d/Y", changeMonth: true,
            changeYear: true, yearRange: '1900:2020', defaultDate: ''}).val("");
			}
		});
	}

	const datePicker = (val) => {
		sendRequest("coral/", {"val" : val, "state" : "2"}, (results) => {
			let val = $("#datepicker").val();
			$_merchant.text(results[0].merchant);
			$_impression.text(results[0].impreto);
			$_click.text(results[0].clito);
			$_registration.text(results[0].regto);
			$_depo.text(results[0].ndto);
			$_commission.text("£ " + results[0].commito);
			$("#title").text("Quick Stats at a Glance | " + val);
			$(".periodpicker").children().remove();
			$(".periodpicker").append(
				$("<option/>")
                    .text("Select one of the following...")
                    .css({display: "none"})
                    .prop({
                        selected: true,
                        disabled: true
                    }),
                $("<option>")
                	.val("1")
                	.text("MTD"),
                $("<option>")
                	.val("2")
                	.text("YTD"),
			);
		});
	}

	const init = () => {
		$(document)
		.on("change", ".periodpicker", (event) => {
			let val = $_periodpicker.val();
			periodpicker(val);
		})

		.on("change", "#datepicker", (event) => {
			let val = $("#datepicker").val();
			datePicker(val);
		})
	}

	return {
		init : init
	}
})();

((window, $) => {
	Coral.init();
})(window, jQuery);

$(function () {
  $('#reservation').daterangepicker()
  //Date range picker with time picker
  $('#reservationtime').daterangepicker({ timePicker: true, timePickerIncrement: 30, format: 'MM/DD/YYYY h:mm A' })
  //Date range as a button
  $('#daterange-btn').daterangepicker(
    {
      ranges   : {
        'Today'       : [moment(), moment()],
        'Yesterday'   : [moment().subtract(1, 'days'), moment().subtract(1, 'days')],
        'Last 7 Days' : [moment().subtract(6, 'days'), moment()],
        'Last 30 Days': [moment().subtract(29, 'days'), moment()],
        'This Month'  : [moment().startOf('month'), moment().endOf('month')],
        'Last Month'  : [moment().subtract(1, 'month').startOf('month'), moment().subtract(1, 'month').endOf('month')]
      },
      startDate: moment().subtract(29, 'days'),
      endDate  : moment()
    },
    function (start, end) {
      $('#daterange-btn span').html(start.format('MMMM D, YYYY') + ' - ' + end.format('MMMM D, YYYY'))
    }
  )

  //Date picker
  $('#datepicker').datepicker({
    autoclose: true
  })

})