function display_live_alerts(url) {
    fetch(url)
        .then(function (response) {
        if (!response.ok) {
            new Error('Data not sent');
        }
        return response.json();
    })
        .then(function (data) {
        var liveAlertsContainers = document.getElementById('live-alerts-container');
        var queueStats = document.querySelector('#queue-stats');
        if (!liveAlertsContainers && !queueStats)
            return;
        liveAlertsContainers.innerHTML = '';
        if (data === null) {
            liveAlertsContainers.insertAdjacentHTML('afterbegin', "<div>No alerts yet.</div>");
        }
        queueStats.insertAdjacentHTML('beforeend', "<span>".concat(data.totalActiveAlerts, "</span>"));
        var userId = Number(data.alerts[0].user_id);
        data.alerts.forEach(function (displayAlert) {
            liveAlertsContainers.insertAdjacentHTML('beforeend', "<div class=\"bg-admin-midnight-navy-blue border border-admin-muted-denim-blue\n                            hover:bg-admin-deep-navy-blue px-4 py-2 space-y-2 h-36 overflow-y-hidden\">\n                                <div class=\"flex items-center justify-between\">\n                                    <div class=\"space-x-4\">\n                                        <span>Alert</span>\n                                        <span>#".concat(displayAlert.id, "</span>\n                                    </div>\n                                    <div>\n                                        <span class=\"text-bold\">Typing CPS: ").concat(displayAlert.typing_speed_cps, "</span>\n                                    </div>\n                                </div>\n                                <div class=\"flex items-center justify-between\">\n                                    <div class=\"space-x-6\">\n                                        <span>").concat(displayAlert.user_id ? "User Id: ".concat(displayAlert.user_id) : 'User_id', "</span>\n                                    </div>\n                                    <div>\n                                        <span class=\"text-admin-muted-slate-gray\">").concat(formatDate(displayAlert.timestamp), "</span>\n                                    </div>\n                                </div>\n                                <div class=\"flex items-center space-x-2\">\n                                    <span>Desciption: ").concat(displayAlert.description, "</span>\n                                </div>\n                            </div>"));
        });
        transactionHistoryTimeline("/system-admin/user-data-and-timeline/".concat(userId));
        behavioralSignals("/system-admin/user-data-and-timeline/".concat(userId));
    })
        .catch(function (error) {
        console.error('Dashboard Error:', error);
    });
}
function formatDate(timestamp) {
    var date = new Date(timestamp);
    var alertDate = date.toLocaleString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
    });
    return alertDate;
}
function behavioralSignals(url) {
    try {
        fetch(url)
            .then(function (response) {
            if (!response.ok)
                throw new Error('Error fetching json data');
            return response.json();
        })
            .then(function (data) {
            var behaviorSignalsContainer = document.getElementById('behavior-signals-container');
            if (!behaviorSignalsContainer)
                return;
            behaviorSignalsContainer.innerHTML = '';
            data.devices_tracked.forEach(function (sentData) {
                behaviorSignalsContainer.insertAdjacentHTML('beforeend', "<li class=\"flex items-center space-x-2\">\n                            <svg class=\"fill-current w-2 text-admin-off-white\" xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 122.88 122.88\">\n                            <path fill-rule=\"evenodd\" clip-rule=\"evenodd\" d=\"M61.438,0c33.93,0,61.441,27.512,61.441,61.441 c0,33.929-27.512,61.438-61.441,61.438C27.512,122.88,0,95.37,0,61.441C0,27.512,27.512,0,61.438,0L61.438,0z\"/>\n                            </svg>\n                            <span>Device Status: ".concat(sentData.device_age_status, "</span>\n                        </li>\n                        <li class=\"flex items-center space-x-2\">\n                            <svg class=\"fill-current w-2 text-admin-off-white\" xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 122.88 122.88\">\n                            <path fill-rule=\"evenodd\" clip-rule=\"evenodd\" d=\"M61.438,0c33.93,0,61.441,27.512,61.441,61.441 c0,33.929-27.512,61.438-61.441,61.438C27.512,122.88,0,95.37,0,61.441C0,27.512,27.512,0,61.438,0L61.438,0z\"/>\n                            </svg>\n                            <span>Device Model: ").concat(sentData.device_model, "</span>\n                        </li>\n                        <li class=\"flex items-center space-x-2\">\n                            <svg class=\"fill-current w-2 text-admin-off-white\" xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 122.88 122.88\">\n                            <path fill-rule=\"evenodd\" clip-rule=\"evenodd\" d=\"M61.438,0c33.93,0,61.441,27.512,61.441,61.441 c0,33.929-27.512,61.438-61.441,61.438C27.512,122.88,0,95.37,0,61.441C0,27.512,27.512,0,61.438,0L61.438,0z\"/>\n                            </svg>\n                            <span>Rooted or Jailbroken: ").concat(sentData.is_rooted_or_jailbroken, "</span>\n                        </li>\n                        <hr class\"text-admin-off-white\">"));
            });
        });
    }
    catch (error) {
        console.error(error);
    }
}
function transactionHistoryTimeline(url) {
    try {
        fetch(url)
            .then(function (response) {
            if (!response.ok)
                throw new Error('Error fetching json data');
            return response.json();
        })
            .then(function (data) {
            var transactionHistoryContainer = document.getElementById('transaction-history-container');
            if (!transactionHistoryContainer)
                return;
            transactionHistoryContainer.innerHTML = '';
            data.transaction_history.forEach(function (sentData) {
                transactionHistoryContainer.insertAdjacentHTML('beforeend', "<li class=\"flex items-center space-x-2\">\n                            <svg class=\"fill-current w-2 text-admin-off-white\" xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 122.88 122.88\">\n                            <path fill-rule=\"evenodd\" clip-rule=\"evenodd\" d=\"M61.438,0c33.93,0,61.441,27.512,61.441,61.441 c0,33.929-27.512,61.438-61.441,61.438C27.512,122.88,0,95.37,0,61.441C0,27.512,27.512,0,61.438,0L61.438,0z\"/>\n                            </svg>\n                            <span>Event Type: ".concat(sentData.event_type, "</span>\n                        </li>\n                        <li class=\"flex items-center space-x-2\">\n                            <svg class=\"fill-current w-2 text-admin-off-white\" xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 122.88 122.88\">\n                            <path fill-rule=\"evenodd\" clip-rule=\"evenodd\" d=\"M61.438,0c33.93,0,61.441,27.512,61.441,61.441 c0,33.929-27.512,61.438-61.441,61.438C27.512,122.88,0,95.37,0,61.441C0,27.512,27.512,0,61.438,0L61.438,0z\"/>\n                            </svg>\n                            <span>Description: ").concat(sentData.description, "</span>\n                        </li>\n                        <li class=\"flex items-center space-x-2\">\n                            <svg class=\"fill-current w-2 text-admin-off-white\" xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 122.88 122.88\">\n                            <path fill-rule=\"evenodd\" clip-rule=\"evenodd\" d=\"M61.438,0c33.93,0,61.441,27.512,61.441,61.441 c0,33.929-27.512,61.438-61.441,61.438C27.512,122.88,0,95.37,0,61.441C0,27.512,27.512,0,61.438,0L61.438,0z\"/>\n                            </svg>\n                            <span>").concat(formatDate(sentData.timestamp), "</span>\n                        </li>\n                        <hr class\"text-admin-off-white\">"));
            });
        });
    }
    catch (error) {
        console.error(error);
    }
}
document.addEventListener('DOMContentLoaded', function () {
    display_live_alerts('/system-admin/admin-dashboard');
});
