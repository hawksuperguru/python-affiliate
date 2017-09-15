let DatabasePage = (() => {
    const init = () => {
        $(document)
        .on("click", "#db-backup", () => {
            AffiliateAPI.backup()
        })
    }

    return {
        init: init
    }
})();

((window, $) => {
	DatabasePage.init();
})(window, jQuery);