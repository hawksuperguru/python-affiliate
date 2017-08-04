  (($) => {
    window.bet365Table = $('#table-365').DataTable( {     
      "scrollY": 400,
      "scrollX": true,
      "fnFooterCallback": function( nFoot, aData, iStart, iEnd, aiDisplay ) {
        let footEls = nFoot.getElementsByTagName('th');
        footEls[1].innerHTML = (window.Bet365 || {}).sClick || "";
        footEls[2].innerHTML = (window.Bet365 || {}).sSignup || "";
        footEls[3].innerHTML = (window.Bet365 || {}).sNdepo || "";
        footEls[4].innerHTML = (window.Bet365 || {}).sValdepo || "";
        footEls[5].innerHTML = (window.Bet365 || {}).sNumdepo || "";
        footEls[6].innerHTML = (window.Bet365 || {}).sSpotsTurn || "";
        footEls[7].innerHTML = (window.Bet365 || {}).sNumsptbet || "";
        footEls[8].innerHTML = (window.Bet365 || {}).sAcsptusr || "";
        footEls[9].innerHTML = (window.Bet365 || {}).sSptnetrev || "";
        footEls[10].innerHTML = (window.Bet365 || {}).sCasinonetrev || "";
        footEls[11].innerHTML = (window.Bet365 || {}).sPokernetrev || "";
        footEls[12].innerHTML = (window.Bet365 || {}).sBingonetrev || "";
        footEls[13].innerHTML = (window.Bet365 || {}).sNetrev || "";
        footEls[14].innerHTML = (window.Bet365 || {}).sAfspt || "";
        footEls[15].innerHTML = (window.Bet365 || {}).sAfcasino || "";
        footEls[16].innerHTML = (window.Bet365 || {}).sAfpoker || "";
        footEls[17].innerHTML = (window.Bet365 || {}).sAfbingo || "";
        footEls[18].innerHTML = (window.Bet365 || {}).sCommission || "";
        footEls[0].innerHTML = "Total : ";
      }
    } );

    $(document)
    .on("click", '.applyBtn', (event) => {
        sendAjax();
    })

    $(document)
    .on("change", '.selectpicker', (event) => {
        sendAjax();
    })
})(jQuery);


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

function sendAjax() {
  let period = $('#reservation').val();
  let optVal = $('.selectpicker').val();
  
  if (optVal == ''){
    optVal = '0';
  }

  $.ajax({
      url: "/bet365/",
      data: JSON.stringify({
          'period' : period,
          'optVal' : optVal
      }),
      contentType: "application/json",
      type: 'POST',
      success: (response) => {
        let $tb = $(".tbody");
        let jsonData = response.jsonData;
        window.bet365Table.rows().remove().draw();

        let sClick = 0, 
            sSignup = 0, 
            sNdepo = 0,
            sValdepo = 0, 
            sNumdepo = 0, 
            sSpotsTurn = 0, 
            sAcsptusr = 0, 
            sNumsptbet = 0, 
            sSptnetrev = 0, 
            sCasinonetrev = 0, 
            sPokernetrev = 0, 
            sBingonetrev = 0, 
            sNetrev = 0, 
            sAfspt = 0, 
            sAfcasino = 0, 
            sAfpoker = 0, 
            sAfbingo = 0, 
            sCommission = 0,
            date = '';

          for(let i = 0; i < jsonData.length; i++){
            string = jsonData[i].dateto;
            expr = /:/;                 
            flag = expr.test(string);
            let date = ''
            
            if (flag){
              let dateObj = new Date(jsonData[i].dateto);
              date = dateObj.getFullYear() + "-" + (dateObj.getMonth() + 1) + "-" + dateObj.getDate();              
            }else{
              date = jsonData[i].dateto;
            }
            
            let tempRow = [
              date,
              jsonData[i].click,
              jsonData[i].nSignup,
              jsonData[i].nDepo,
              jsonData[i].valDepo,
              jsonData[i].numDepo,
              jsonData[i].spotsTurn,
              jsonData[i].numSptBet,
              jsonData[i].acSptUsr,
              jsonData[i].sptNetRev,
              jsonData[i].casinoNetRev,
              jsonData[i].pokerNetRev,
              jsonData[i].bingoNetRev,
              jsonData[i].netRev,
              jsonData[i].afSpt,
              jsonData[i].afCasino,
              jsonData[i].afPoker,
              jsonData[i].afBingo,
              jsonData[i].commission
            ];

            sClick += jsonData[i].click;
            sSignup += jsonData[i].nSignup;
            sNdepo += jsonData[i].nDepo;
            sValdepo += jsonData[i].valDepo;
            sNumdepo += jsonData[i].numDepo;
            sSpotsTurn += jsonData[i].spotsTurn;
            sAcsptusr += jsonData[i].acSptUsr;
            sNumsptbet += jsonData[i].numSptBet;
            sSptnetrev += jsonData[i].sptNetRev;
            sCasinonetrev += jsonData[i].casinoNetRev;
            sPokernetrev += jsonData[i].pokerNetRev;
            sBingonetrev += jsonData[i].bingoNetRev;
            sNetrev += jsonData[i].netRev;
            sAfspt += jsonData[i].afSpt;
            sAfcasino += jsonData[i].afCasino;
            sAfpoker += jsonData[i].afPoker;
            sAfbingo += jsonData[i].afBingo;
            sCommission += jsonData[i].commission;

            window.Bet365 = {
              sClick,
              sSignup,
              sNdepo,
              sValdepo: parseFloat(sValdepo).toFixed(2),
              sNumdepo,
              sSpotsTurn: parseFloat(sSpotsTurn).toFixed(2),
              sAcsptusr,
              sNumsptbet,
              sSptnetrev,
              sCasinonetrev: parseFloat(sCasinonetrev).toFixed(2),
              sPokernetrev: parseFloat(sPokernetrev).toFixed(2),
              sBingonetrev: parseFloat(sBingonetrev).toFixed(2),
              sNetrev: parseFloat(sNetrev).toFixed(2),
              sAfspt: parseFloat(sAfspt).toFixed(2),
              sAfcasino: parseFloat(sAfcasino).toFixed(2),
              sAfpoker: parseFloat(sAfpoker).toFixed(2),
              sAfbingo: parseFloat(sAfbingo).toFixed(2),
              sCommission: parseFloat(sCommission).toFixed(2)
            }

            window.bet365Table.row.add(tempRow).draw();
          }
      },
      error: (error) => {
      }
  });
}