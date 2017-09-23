let Dashboard = ((window, jQuery) => {
    let _mode = "daily",
        _resultsTable = null,
        _dateRange = null;

    const drawTable = (results) => {
        _resultsTable.rows().remove().draw()

        let index = 1
        results.forEach(function(element) {
            let rowData = [
                index,
                element.name,
                element.click,
                element.signup,
                element.commission,
                element.affiliate_click,
                element.affiliate_signup,
                element.affiliate_commission,
            ]
            _resultsTable.row.add(rowData).draw()
            index++
        }, this);
    }

    /**
     * Event Handler for sort drop down option
     * @param {string} value 
     * @return {void}
     */
    const reservationChangeHandler = (value) => {
        _mode = value
        switch(value) {
            case 'daily':
            case 'weekly':
            case 'monthly':
            case 'yearly':
                console.log("Correct")
                $("#date-range-container").addClass("hide")
                AffiliateAPI.get(value, null, drawTable)
                break
            case 'custom':
                $("#date-range-container").removeClass("hide")
                break
        }
    }
    
    /**
     * Initialize Elements like dateRangePicker, dataTable, etc...
     * @return {void}
     */
    const initElements = () => {
        $("#date-range").daterangepicker({
            locale: {
                format: "YYYY/MM/DD",
            },
            changeMonth: true,
            changeYear: true,
            yearRange: '1900:2020'
        })

        _resultsTable = $("#dashboard-results").DataTable()
    }

    /**
     * Initialize jQuery events
     */
    const initEvents = () => {
        $(document)
        .on("change", "#reservations", (event) => {
            event.preventDefault()
            let value = event.target.value;
            reservationChangeHandler(value)
        })
        .on("change", "#date-range", (event) => {
            _dateRange = event.target.value
            AffiliateAPI.get(_mode, _dateRange, drawTable)
        })
    }

    /**
     * Initializer
     */
    const init = () => {
        console.log("Hello, dashboard is being initialized...");
        initElements()
        initEvents()
    }

    return {
        init: init
    }
})(window, $)

$(() => {
    Dashboard.init()
})