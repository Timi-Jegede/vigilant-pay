interface FraudAlert {
    id: number;
    user_id: string;
    amount: string | number;
    typing_speed_cps: string,
    timestamp: string,
    description: string
}

function display_live_alerts(url: string): void {
    fetch(url)
    .then(response => {
        if (!response.ok) {
            new Error('Data not sent');
        }

        return response.json();
    })
    .then((data: {totalActiveAlerts: number, alerts: FraudAlert[]}) => {
        const liveAlertsContainers = document.getElementById('live-alerts-container') as HTMLElement;
        const queueStats = document.querySelector('#queue-stats') as HTMLElement;

        if (!liveAlertsContainers && !queueStats) return;

        liveAlertsContainers.innerHTML = '';

        if (data === null) {
            liveAlertsContainers.insertAdjacentHTML('afterbegin',
                `<div>No alerts yet.</div>`
            )
        }

        queueStats.insertAdjacentHTML('beforeend', `<span>${data.totalActiveAlerts}</span>`);

        const userId: number = Number(data.alerts[0].user_id);

        data.alerts.forEach(displayAlert => {
            liveAlertsContainers.insertAdjacentHTML(
                'beforeend',
                `<div class="bg-admin-midnight-navy-blue border border-admin-muted-denim-blue
                            hover:bg-admin-deep-navy-blue px-4 py-2 space-y-2 h-36 overflow-y-hidden">
                                <div class="flex items-center justify-between">
                                    <div class="space-x-4">
                                        <span>Alert</span>
                                        <span>#${displayAlert.id}</span>
                                    </div>
                                    <div>
                                        <span class="text-bold">Typing CPS: ${displayAlert.typing_speed_cps}</span>
                                    </div>
                                </div>
                                <div class="flex items-center justify-between">
                                    <div class="space-x-6">
                                        <span>${ displayAlert.user_id ? `User Id: ${displayAlert.user_id}` : 'User_id'}</span>
                                    </div>
                                    <div>
                                        <span class="text-admin-muted-slate-gray">${formatDate(displayAlert.timestamp)}</span>
                                    </div>
                                </div>
                                <div class="flex items-center space-x-2">
                                    <span>Desciption: ${displayAlert.description}</span>
                                </div>
                            </div>`
            );
        });
        
        transactionHistoryTimeline(`/system-admin/user-data-and-timeline/${userId}`);
        behavioralSignals(`/system-admin/user-data-and-timeline/${userId}`);
    })
    .catch(error => {
        console.error('Dashboard Error:', error);
    });
}

function formatDate(timestamp: string) {
    const date = new Date(timestamp);

    const alertDate = date.toLocaleString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
    });
   
    return alertDate;
}

interface BehavioralSignal {
    device_age_status: string,
    is_rooted_or_jailbroken: boolean,
    device_model: string
}

function behavioralSignals(url: string): void {
    try {
        fetch(url)
        .then(response => {
            if (!response.ok) throw new Error('Error fetching json data');
            
            return response.json();
        })
        .then((data: {user_id: number, risk_score: Number, devices_tracked: BehavioralSignal[]}) => {
            const behaviorSignalsContainer = document.getElementById('behavior-signals-container') as HTMLElement;

            if (!behaviorSignalsContainer) return;

            behaviorSignalsContainer.innerHTML = '';

            data.devices_tracked.forEach(sentData => {
                behaviorSignalsContainer.insertAdjacentHTML(
                    'beforeend',
                    `<li class="flex items-center space-x-2">
                            <svg class="fill-current w-2 text-admin-off-white" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 122.88 122.88">
                            <path fill-rule="evenodd" clip-rule="evenodd" d="M61.438,0c33.93,0,61.441,27.512,61.441,61.441 c0,33.929-27.512,61.438-61.441,61.438C27.512,122.88,0,95.37,0,61.441C0,27.512,27.512,0,61.438,0L61.438,0z"/>
                            </svg>
                            <span>Device Status: ${sentData.device_age_status}</span>
                        </li>
                        <li class="flex items-center space-x-2">
                            <svg class="fill-current w-2 text-admin-off-white" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 122.88 122.88">
                            <path fill-rule="evenodd" clip-rule="evenodd" d="M61.438,0c33.93,0,61.441,27.512,61.441,61.441 c0,33.929-27.512,61.438-61.441,61.438C27.512,122.88,0,95.37,0,61.441C0,27.512,27.512,0,61.438,0L61.438,0z"/>
                            </svg>
                            <span>Device Model: ${sentData.device_model}</span>
                        </li>
                        <li class="flex items-center space-x-2">
                            <svg class="fill-current w-2 text-admin-off-white" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 122.88 122.88">
                            <path fill-rule="evenodd" clip-rule="evenodd" d="M61.438,0c33.93,0,61.441,27.512,61.441,61.441 c0,33.929-27.512,61.438-61.441,61.438C27.512,122.88,0,95.37,0,61.441C0,27.512,27.512,0,61.438,0L61.438,0z"/>
                            </svg>
                            <span>Rooted or Jailbroken: ${sentData.is_rooted_or_jailbroken}</span>
                        </li>
                        <hr class"text-admin-off-white">`
                );
            });
        });
    } catch (error) {
        console.error(error);
    }
}

interface TransactionHistory {
    event_type: string,
    description: string,
    timestamp: string
}

function transactionHistoryTimeline(url: string): void {
    try {
        fetch(url)
        .then(response => {
            if (!response.ok) throw new Error('Error fetching json data')
            
            return response.json();
        })
        .then((data: {user_id: number, risk_score: Number, transaction_history: TransactionHistory[]}) => {
            const transactionHistoryContainer = document.getElementById('transaction-history-container') as HTMLElement;

            if (!transactionHistoryContainer) return;

            transactionHistoryContainer.innerHTML = '';

            data.transaction_history.forEach(sentData => {
                transactionHistoryContainer.insertAdjacentHTML(
                    'beforeend',
                    `<li class="flex items-center space-x-2">
                            <svg class="fill-current w-2 text-admin-off-white" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 122.88 122.88">
                            <path fill-rule="evenodd" clip-rule="evenodd" d="M61.438,0c33.93,0,61.441,27.512,61.441,61.441 c0,33.929-27.512,61.438-61.441,61.438C27.512,122.88,0,95.37,0,61.441C0,27.512,27.512,0,61.438,0L61.438,0z"/>
                            </svg>
                            <span>Event Type: ${sentData.event_type}</span>
                        </li>
                        <li class="flex items-center space-x-2">
                            <svg class="fill-current w-2 text-admin-off-white" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 122.88 122.88">
                            <path fill-rule="evenodd" clip-rule="evenodd" d="M61.438,0c33.93,0,61.441,27.512,61.441,61.441 c0,33.929-27.512,61.438-61.441,61.438C27.512,122.88,0,95.37,0,61.441C0,27.512,27.512,0,61.438,0L61.438,0z"/>
                            </svg>
                            <span>Description: ${sentData.description}</span>
                        </li>
                        <li class="flex items-center space-x-2">
                            <svg class="fill-current w-2 text-admin-off-white" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 122.88 122.88">
                            <path fill-rule="evenodd" clip-rule="evenodd" d="M61.438,0c33.93,0,61.441,27.512,61.441,61.441 c0,33.929-27.512,61.438-61.441,61.438C27.512,122.88,0,95.37,0,61.441C0,27.512,27.512,0,61.438,0L61.438,0z"/>
                            </svg>
                            <span>${formatDate(sentData.timestamp)}</span>
                        </li>
                        <hr class"text-admin-off-white">`
                );
            });
        });
    } catch(error) {
        console.error(error);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    display_live_alerts('/system-admin/admin-dashboard');
});
