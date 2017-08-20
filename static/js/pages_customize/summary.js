let Summary = (() => {
	const _baseUrl = "/";
	let $_selectPicker = $(".selectpicker");
	let $tB3Odate = $("#tB3Odate");
	let $tB3Oclick = $("#tB3Oclick");
	let $tB3Osignup = $("#tB3Osignup");
	let $tB3Odepo = $("#tB3Odepo");
	let $tB3Odollar = $("#tB3Odollar");
	let $tB3date = $("#tB3date");
	let $tB3click = $("#tB3click");
	let $tB3signup = $("#tB3signup");
	let $tB3depo = $("#tB3depo");
	let $tB3dollar = $("#tB3dollar");
	let $t8click = $("#t8click");
	let $t8register = $("#t8register");
	let $t8balance = $("#t8balance");
	let $t8dollar = $("#t8dollar");
	let $tB10click = $("#tB10click");
	let $tB10register = $("#tB10register");
	let $tB10commission = $("#tB10commission");
	let $tB10dollar = $("#tB10dollar");
	let $tRealclick = $("#tRealclick");
	let $tRealregister = $("#tRealregister");
	let $tRealcommission = $("#tRealcommission");
	let $tRealdollar = $("#tRealdollar");
	let $tSkyclick = $("#tSkyclick");
	let $tSkyregister = $("#tSkyregister");
	let $tSkycommission = $("#tSkycommission");
	let $tSkydollar = $("#tSkydollar");
	let $tWildollar = $("#tWildollar");
	let $tLadollar = $("#tLadollar");
	let $tPadollar = $("#tPadollar");
	let $tNetdollar = $("#tNetdollar");
	let $tTidollar = $("#tTidollar");
	let $tStanclick = $("#tStanclick");
	let $tStanregister = $("#tStanregister");
	let $tStancommission = $("#tStancommission");
	let $tStandollar = $("#tStandollar");
	let $tCoralclick = $("#tCoralclick");
	let $tCoralregister = $("#tCoralregister");
	let $tCoralcommission = $("#tCoralcommission");
	let $tCoraldollar = $("#tCoraldollar");
	let $tBFclick = $("#tBFclick");
	let $tBFregister = $("#tBFregister");
	let $tBFcommission = $("#tBFcommission");
	let $tBFdollar = $("#tBFdollar");
	let $total = $("#total");

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
		sendRequest("summary/", {"val" : val}, (results) => {
			let val = $_selectPicker.val();
			$tB3Odate.text(results[0].tB3Odate);
			$tB3Oclick.text(results[0].tB3Oclick);
			$tB3Osignup.text(results[0].tB3Osignup);
			$tB3Odepo.text(results[0].tB3Odepo);
			$tB3Odollar.text(results[0].tB3Odollar);

			$tB3date.text(results[0].tB3date);
			$tB3click.text(results[0].tB3click);
			$tB3signup.text(results[0].tB3signup);
			$tB3depo.text(results[0].tB3depo);
			$tB3dollar.text(results[0].tB3dollar);

			$t8click.text(results[0].t8click);
			$t8register.text(results[0].t8register);
			$t8balance.text(results[0].t8balance);
			$t8dollar.text(results[0].t8dollar);

			$tB10click.text(results[0].clito);
			$tB10register.text(results[0].regto);
			$tB10commission.text(results[0].commito);
			$tB10dollar.text(results[0].tB10dollar);

			$tRealclick.text(results[0].clito);
			$tRealregister.text(results[0].regto);
			$tRealcommission.text(results[0].commito);
			$tRealdollar.text(results[0].tRealdollar);

			$tSkyclick.text(results[0].clito);
			$tSkyregister.text(results[0].regito);
			$tSkycommission.text(results[0].commito);
			$tSkydollar.text(results[0].tSkydollar);

			$tWildollar.text(results[0].tWildollar);

			$tLadollar.text(results[0].tLadollar);

			$tPadollar.text(results[0].tPadollar);

			$tNetdollar.text(results[0].tNetdollar);

			$tTidollar.text(results[0].tTidollar);

			$tStanclick.text(results[0].clito);
			$tStanregister.text(results[0].regto);
			$tStancommission.text(results[0].commito);
			$tStandollar.text(results[0].tStandollar);

			$tCoralclick.text(results[0].clito);
			$tCoralregister.text(results[0].regto);
			$tCoralcommission.text(results[0].commito);
			$tCoraldollar.text(results[0].tCoraldollar);

			$tBFclick.text(results[0].clito);
			$tBFregister.text(results[0].regto);
			$tBFcommission.text(results[0].commito);
			$tBFdollar.text(results[0].tBFdollar);

			$total.text(results[0].total)
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
	Summary.init();
})(window, jQuery);