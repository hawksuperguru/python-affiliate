let Dashboard = ((window, jQuery) => {
    const reservationChangeHandler = (value) => {
        switch(value) {
            case 'daily':
            case 'weekly':
            case 'monthly':
            case 'yearly':
                console.log("Correct")
                $("#date-range-container").addClass("hide")
                break
            case 'custom':
                $("#date-range-container").removeClass("hide")
                break
        }
    }
    const init = () => {
        console.log("Hello, dashboard is being initialized...");
        $("#date-range").daterangepicker({
            locale: {
                format: "YYYY/MM/DD",
            },
            changeMonth: true,
            changeYear: true,
            yearRange: '1900:2020'
        })
        $(document)
        .on("change", "#reservations", (event) => {
            event.preventDefault()
            let value = event.target.value;
            reservationChangeHandler(value)
        })
    }

    return {
        init: init
    }
})(window, $)

$(() => {
    Dashboard.init()
})