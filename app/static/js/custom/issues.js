let Issues = ((window, jQuery) => {
    let _dataTable = null

    const init = () => {
        _dataTable = $("#issues-table").DataTable()

        $("#issues-table")
        .on("click", ".btn-mark-as-solved", (event) => {
            let id = event.target.getAttribute('data-id'),
                $record = $(event.target).parents("tr")

            if (confirm("Are you sure to mark this issue as 'solved'?")) {
                AffiliateAPI.manageIssue(id, (response) => {
                    $(event.target).removeClass("btn-primary").addClass("btn-danger")
                    .removeClass("btn-mark-as-solved").addClass("btn-undo")
                    .text("Undo")

                    $issuesCount = $("#notification-issues-count");
                    $issuesCount.text(Math.max(parseInt($issuesCount.text()) - 1, 0))
                })
            }
        })
        .on("click", ".btn-undo", (event) => {
            let id = event.target.getAttribute('data-id'),
                $record = $(event.target).parents("tr")

            AffiliateAPI.undoIssue(id, (response) => {
                $(event.target).removeClass("btn-danger").addClass("btn-primary")
                .removeClass("btn-undo").addClass("btn-mark-as-solved")
                .text("Mark as solved")

                $issuesCount = $("#notification-issues-count");
                $issuesCount.text(Math.max(parseInt($issuesCount.text()) + 1, 0))
            })
        })
    }

    return {
        init: init
    }
})(window, $)

$(() => {
    Issues.init()
})