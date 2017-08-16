let Bet10 = (() => {
	const _baseUrl = '/';
	let $_selectPicker = $(".selectpicker");
	let $_merchant = $("#merchant");
	let $_impression = $("#_impression");
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
				}
				else if (typeof callback === 'function') {
						callback(response.jsonData);
				}
			},
			error : (error) => {
				alert("failure");
			},
		});
	}

	const selectPicker = (val) => {
		sendRequest("bet10/", {"val" : val}, (results) => {
			let val = $_selectPicker.val();
			console.log(results)
			if (val == 1) {
				$_impression.text(results[0].impression);
				$_click.text(results[0].click);
				$_registration.text(results[0].registration);
				$_depo.text(results[0].new_deposit);
				$_commission.text("£ " + results[0].commission);
				$("#title").text("Stats at a Glance | MTD");
			}
			else if (val == 2) {
				$_impression.text(results[0].impreytd);
				$_click.text(results[0].cliytd);
				$_registration.text(results[0].regytd);
				$_depo.text(results[0].ndytd);
				$_commission.text("£ " + results[0].commiytd);
				$("#title").text("Stats at a Glance | YTD");
			}
			else if (val == 3) {	
				$_impression.text(results[0].impreto);
				$_click.text(results[0].clito);
				$_registration.text(results[0].regto);
				$_depo.text(results[0].ndto);
				$_commission.text("£ " + results[0].commito);
				$("#title").text("Stats at a Glance | TODAY");
			}
		});
	}

	const init = () => {
		$(document)
		.on("change", ".selectpicker", (event) => {
			let val = $_selectPicker.val();
			selectPicker(val);
		})
	}

	return {
		init : init
	}
})();

((window, $) => {
	Bet10.init();
})(window, jQuery);