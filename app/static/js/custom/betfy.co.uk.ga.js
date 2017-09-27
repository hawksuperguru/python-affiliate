

(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','https://www.google-analytics.com/analytics.js','ga');

$((window, jQuery) => {
    ga('create', 'UA-87760128-1', 'auto');
    ga('send', 'pageview');
    
    let outBoundClickHandler = (anchor) => {
        if (!anchor.href) {
            return false;
        }
        let url = new URL(anchor.href);
        let path = url.pathname;
        let match = path.match(/\/sites\/(.+)\//g);
        
        if (match) {
            let affiliate = match[0].split("/")[2];
            console.log(affiliate + " clicked.");
            ga('send', 'event', 'outbound', affiliate, {
                'transport': 'beacon',
                'hitCallback': function(){
                    document.location = url;
                }
           });
        }
    }
    $(document)
    .on("click", "div.company-logo a.visit-ws *", (event) => {
        event.preventDefault();
        let anchor = $(event.target).parents("a.visit-ws")[0];
        outBoundClickHandler(anchor);
    })
    .on("click", "div.company-logo a.visit-ws", (event) => {
        event.preventDefault();
        outBoundClickHandler(event.target);
    })
})