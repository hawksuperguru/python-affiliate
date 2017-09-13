/**
 * Common Class for API calls
 */
let AffiliateAPI = (() => {
    let _baseUrl = "/";

    /**
     * Function to send Ajax request to API server embedded in affiliate system.
     * @param {string} endPoint 
     * @param {{object}} params 
     * @param {function} success 
     * @param {function} failure 
     */
    const sendRequest = (endPoint, params, success, failure) => {
		$.ajax({
			url : getBaseUrl() + endPoint,
			data : JSON.stringify(params),
			contentType : "application/json",
			type : "POST",
			success : (response) => {
				if (response.status) {
                    (typeof success == "function") && success(response.data)
                } else {
                    (typeof failure == "function") && failure()
                }
			},
			error : (error) => {
				failure(error)
			},
		});
    }

    /**
     * Get API's base url
     */
    const getBaseUrl = () => _baseUrl

    /**
     * Function to mark issue as "Resolved" in issues page
     * @param {number} id 
     * @param {function} success 
     * @param {function} failure 
     */
    const manageIssue = (id, success, failure) => {
        if (parseInt(id) == NaN) {
            failure()
        } else {
            sendRequest("settings/issues/manage", { id },
            success,
            failure)
        }
    }
    
    /**
     * Set base url
     * @param {string} baseURL 
     */
    const init = (baseURL) => {
        _baseUrl = baseURL;
    }

    return {
        init: init,
        manageIssue: manageIssue
    }
})();