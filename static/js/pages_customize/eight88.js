let Eight88 = (() => {
	const _baseUrl = "/";
	let $_selectPicker = $(".selectpicker");
	let $_impression = $("#impression");
	let $_click = $("#click");
	let $_registration = $("#registration");
	let $_lead = $("#lead");
	let $_money_player = $("#money_player");
	let $_balance = $("#balance");

	const sendRequest = (endPoint, params, callback) => {
		$.ajax({
			url: _baseUrl + endPoint,
			data: JSON.stringify(params),
			contentType: "application/json",
			type: 'POST',
			success: (response) => {
				if (!response.status) {
					alert(response.message);
				}
				else if (typeof callback === 'function') {
					callback(response.jsonData);
				}
			},
			error: (error) => {
				alert("failure");
				
			},
		});
	}

	const selectPicker = (val) => {
		sendRequest("eight88/", {"val" : val}, (results) => {
			let val = $_selectPicker.val();
			if (val == 1){
				$_impression.text(results[0].impression);
				$_click.text(results[0].click);
				$_registration.text(results[0].registration);
				$_lead.text(results[0].lead);
				$_money_player.text(results[0].money_player);
				$_balance.text("$" + results[0].balance);
				$("#title").text("Stats at a Glance | This Month (1st - Today)")
			}
			else if (val == 2){
				$_impression.text(results[0].imprwk);
				$_click.text(results[0].cliwk);
				$_registration.text(results[0].regwk);
				$_lead.text(results[0].leadwk);
				$_money_player.text(results[0].mpwk);
				$_balance.text("$" + results[0].balance);
				$("#title").text("Stats at a Glance | Last 7 Days")
			}
			else if (val == 3){
				$_impression.text(results[0].imprpre);
				$_click.text(results[0].clipre);
				$_registration.text(results[0].regpre);
				$_lead.text(results[0].leadpre);
				$_money_player.text(results[0].mppre);
				$_balance.text("$" + results[0].prebalance);
				$("#title").text("Stats at a Glance | Previous Month")
			}
			else if (val == 4){
				$_impression.text(results[0].imprto);
				$_click.text(results[0].clito);
				$_registration.text(results[0].regto);
				$_lead.text(results[0].leadto);
				$_money_player.text(results[0].mpto);
				$_balance.text("$" + results[0].balance);
				$("#title").text("Stats at a Glance | Today")
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
	Eight88.init();
})(window, jQuery);