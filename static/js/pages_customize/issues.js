let Issues = (() => {
    /**
     * Initialize Issues object.
     */
    const init = () => {
        $(document)
        .on("click", "button.manage-issue", (event) => {
            let id = event.target.getAttribute("data-issue-id");
            AffiliateAPI.manageIssue(id, (response) => {
                $table = $(event.target).parents("tbody")
                $(event.target).parents("tr").remove()

                let $records = $table.find("tr")
                for (let i = 0; i < $records.length; i ++) {
                    $records.eq(i).find("td[data-target='index']").text(i + 1)
                }

                let $issuesCount = $("#notification-issues-count");
                let count = Math.max(0, parseInt($issuesCount.text()) - 1)
                $issuesCount.text(count)
            })
        })
    }
    return {
        init: init
    }
})();

((window, $) => {
	Issues.init();
})(window, jQuery);