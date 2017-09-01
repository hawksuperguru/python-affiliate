let Summary = (() => {
	const _baseUrl = "/";
	let $_periodpicker = $(".periodpicker");
	let $tB3Oclick = $("#tB3Oclick");
	let $tB3Osignup = $("#tB3Osignup");
	let $tB3Odepo = $("#tB3Odepo");
	let $tB3Odollar = $("#tB3Odollar");
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
	let $tViclick = $("#tViclick");
	let $tViregister = $("#tViregister");
	let $tVicommission = $("#tVicommission");
	let $tVidollar = $("#tVidollar");
	let $total = $("#total");

	const sendRequest = (endPoint, params, callback) => {
		$.ajax({
			url : _baseUrl + endPoint,
			data : JSON.stringify(params),
			contentType : "application/json",
			type : "POST",
			success : (response) => {
				if (!response.status) {
					alert(response.message);
					$tB3Oclick.text("");
					$tB3Osignup.text("");
					$tB3Odepo.text("");
					$tB3Odollar.text("");
					$tB3click.text("");
					$tB3signup.text("");
					$tB3depo.text("");
					$tB3dollar.text("");
					$t8click.text("");
					$t8register.text("");
					$t8balance.text("");
					$t8dollar.text("");
					$tB10click.text("");
					$tB10register.text("");
					$tB10commission.text("");
					$tB10dollar.text("");
					$tRealclick.text("");
					$tRealregister.text("");
					$tRealcommission.text("");
					$tRealdollar.text("");
					$tSkyclick.text("");
					$tSkyregister.text("");
					$tSkycommission.text("");
					$tSkydollar.text("");
					$tWildollar.text("");
					$tLadollar.text("");
					$tPadollar.text("");
					$tNetdollar.text("");
					$tTidollar.text("");
					$tStanclick.text("");
					$tStanregister.text("");
					$tStancommission.text("");
					$tStandollar.text("");
					$tCoralclick.text("");
					$tCoralregister.text("");
					$tCoralcommission.text("");
					$tCoraldollar.text("");
					$tBFclick.text("");
					$tBFregister.text("");
					$tBFcommission.text("");
					$tBFdollar.text("");
					$total.text("");
					$tViclick.text("");
					$tViregister.text("");
					$tVicommission.text("");
					$tVidollar.text("");
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

	const selectPicker = (val) => {
		sendRequest("dashboard/", {"val" : val, "state" : "2"}, (results) => {
			let val = $_periodpicker.val();
			$tB3Oclick.text(results[0].tB3Oclick);
			$tB3Osignup.text(results[0].tB3Osignup);
			$tB3Odepo.text(results[0].tB3Odepo);
			$tB3Odollar.text(results[0].tB3Odollar);

			$tB3click.text(results[0].tB3click);
			$tB3signup.text(results[0].tB3signup);
			$tB3depo.text(results[0].tB3depo);
			$tB3dollar.text(results[0].tB3dollar);

			$t8click.text(results[0].t8click);
			$t8register.text(results[0].t8register);
			$t8balance.text(results[0].t8balance);
			$t8dollar.text(results[0].t8dollar);

			$tB10click.text(results[0].tB10click);
			$tB10register.text(results[0].tB10register);
			$tB10commission.text(results[0].tB10commission);
			$tB10dollar.text(results[0].tB10dollar);

			$tRealclick.text(results[0].tRealclick);
			$tRealregister.text(results[0].tRealregister);
			$tRealcommission.text(results[0].tRealcommission);
			$tRealdollar.text(results[0].tRealdollar);

			$tSkyclick.text(results[0].tSkyclick);
			$tSkyregister.text(results[0].tSkyregister);
			$tSkycommission.text(results[0].tSkycommission);
			$tSkydollar.text(results[0].tSkydollar);

			$tWildollar.text(results[0].tWildollar);

			$tLadollar.text(results[0].tLadollar);

			$tPadollar.text(results[0].tPadollar);

			$tNetdollar.text(results[0].tNetdollar);

			$tTidollar.text(results[0].tTidollar);

			$tStanclick.text(results[0].tStanclick);
			$tStanregister.text(results[0].tStanregister);
			$tStancommission.text(results[0].tStancommission);
			$tStandollar.text(results[0].tStandollar);

			$tCoralclick.text(results[0].tCoralclick);
			$tCoralregister.text(results[0].tCoralregister);
			$tCoralcommission.text(results[0].tCoralcommission);
			$tCoraldollar.text(results[0].tCoraldollar);

			$tBFclick.text(results[0].tBFclick);
			$tBFregister.text(results[0].tBFregister);
			$tBFcommission.text(results[0].tBFcommission);
			$tBFdollar.text(results[0].tBFdollar);

			$tViclick.text(results[0].tViclick);
			$tViregister.text(results[0].tViregister);
			$tVicommission.text(results[0].tVicommission);
			$tVidollar.text(results[0].tVidollar);

			// $total.text(results[0].total)
			let totalVal = 0;
			$_selector = $("tbody tr").find(".bg-gray");
			$_selector.each(function(){
				indiVal = parseFloat($(this).html());
				if (indiVal >= 0){
					totalVal += indiVal;
					$(this).attr({"style" : "color : black;"});
				}else{
					$(this).attr({"style" : "color : red;"})
				}
				$total.text(Math.round(totalVal * 100) / 100);
			});
			$("#reservation").datepicker({ dateFormat: "m/d/Y", changeMonth: true,
            changeYear: true, yearRange: '1900:2020', defaultDate: ''}).val("");			
		});
	}

	const datePicker = (val) => {
		sendRequest("dashboard/", {"val" : val, "state" : "1"}, (results) => {
			let val = $("#reservation").val();
			$tB3Oclick.text(results[0].tB3Oclick);
			$tB3Osignup.text(results[0].tB3Osignup);
			$tB3Odepo.text(results[0].tB3Odepo);
			$tB3Odollar.text(results[0].tB3Odollar);

			$tB3click.text(results[0].tB3click);
			$tB3signup.text(results[0].tB3signup);
			$tB3depo.text(results[0].tB3depo);
			$tB3dollar.text(results[0].tB3dollar);

			$t8click.text(results[0].t8click);
			$t8register.text(results[0].t8register);
			$t8balance.text(results[0].t8balance);
			$t8dollar.text(results[0].t8dollar);

			$tB10click.text(results[0].tB10click);
			$tB10register.text(results[0].tB10register);
			$tB10commission.text(results[0].tB10commission);
			$tB10dollar.text(results[0].tB10dollar);

			$tRealclick.text(results[0].tRealclick);
			$tRealregister.text(results[0].tRealregister);
			$tRealcommission.text(results[0].tB10commission);
			$tRealdollar.text(results[0].tRealdollar);

			$tSkyclick.text(results[0].tSkyclick);
			$tSkyregister.text(results[0].tSkyregister);
			$tSkycommission.text(results[0].tSkycommission);
			$tSkydollar.text(results[0].tSkydollar);

			$tWildollar.text(results[0].tWildollar);

			$tLadollar.text(results[0].tLadollar);

			$tPadollar.text(results[0].tPadollar);

			$tNetdollar.text(results[0].tNetdollar);

			$tTidollar.text(results[0].tTidollar);

			$tStanclick.text(results[0].tStanclick);
			$tStanregister.text(results[0].tStanregister);
			$tStancommission.text(results[0].tStancommission);
			$tStandollar.text(results[0].tStandollar);

			$tCoralclick.text(results[0].tCoralclick);
			$tCoralregister.text(results[0].tCoralregister);
			$tCoralcommission.text(results[0].tCoralcommission);
			$tCoraldollar.text(results[0].tCoraldollar);

			$tBFclick.text(results[0].tBFclick);
			$tBFregister.text(results[0].tBFregister);
			$tBFcommission.text(results[0].tBFcommission);
			$tBFdollar.text(results[0].tBFdollar);

			$tViclick.text(results[0].tViclick);
			$tViregister.text(results[0].tViregister);
			$tVicommission.text(results[0].tVicommission);
			$tVidollar.text(results[0].tVidollar);


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
			let totalVal = 0;
			$_selector = $("tbody tr").find(".bg-gray");
			$_selector.each(function(){
				indiVal = parseFloat($(this).html());
				if (indiVal >= 0){
					totalVal += indiVal;
					$(this).attr({"style" : "color : black;"});
				}else{
					$(this).attr({"style" : "color : red;"})
				}
				$total.text(Math.round(totalVal * 100) / 100);
			});
		});
	}

	const init = () => {
		let totalVal = 0;
		$_selector = $("tbody tr").find(".bg-gray");
		$_selector.each(function(){
			indiVal = parseFloat($(this).html());
			if (indiVal >= 0){
				totalVal += indiVal;
				$(this).attr({"style" : "color : black;"});
			}else{
				$(this).attr({"style" : "color : red;"})
			}
			$total.text(Math.round(totalVal * 100) / 100);
		});

		$(document)
		.on("change", ".periodpicker", (event) => {
			let val = $_periodpicker.val();
			selectPicker(val);
		})

		.on("click", ".applyBtn", (event) => {
			let val = $("#reservation").val();
			datePicker(val);
		})
	}

	return {
		init : init
	}
})();

((window, $) => {
	Summary.init();
})(window, jQuery);

$(function () {
  $("#reservation").daterangepicker({ dateFormat: "m/d/Y", changeMonth: true,
            changeYear: true, yearRange: '1900:2020', defaultDate: ''}).val("");
})