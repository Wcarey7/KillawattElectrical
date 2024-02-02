////////////////////////////////////////////////////////////////////////////////////////////////////
// Logs user out automatically when session expires if there is no activity.
// Provides a warning modal prior to session expiring.
// 
// Source: Adapted from Github user saltycrane
// https://github.com/saltycrane/session-timeout-example/blob/master/static/session-monitor.js
////////////////////////////////////////////////////////////////////////////////////////////////////
sessionMonitor = function(options) {
    "use strict";

    let loc = document.location;
    let originUrl = loc.origin;

    let defaults = {
            // ( 30 minutes in milliseconds)
            sessionLifetime: configSessionLifetime,
            // ( 5 minutes in milliseconds)
            timeBeforeWarning: configSessionLifetime - (25 * 60 * 1000),
            // Minimum time between pings to the server ( 2 minutes in milliseconds)
            minPingInterval: 2 * 60 * 1000,
            // Space-separated list of events passed to $(document).on() that indicate a user is active
            activityEvents: 'mouseup',
            // URL to ping the server using HTTP POST to extend the session
            pingUrl: `${originUrl}/auth/ping/`,
            // URL used to log out when the user clicks a "Log out" button
            logoutUrl: `${originUrl}/auth/logout/`,
            // URL used to log out when the session times out
            timeoutUrl: `${originUrl}/auth/session-timed-out/`,
            ping() {
                // Ping the server to extend the session expiration using a POST request.
                $.ajax({
                    type: 'POST',
                    url: self.pingUrl,
                    beforeSend: function(jqXHR) {
                        jqXHR.setRequestHeader('X-CSRFToken', csrf_token);
                    }
                });
            },
            logout() {
                // Go to the logout page.
                window.location.href = self.logoutUrl;
            },
            onwarning() {
                // Warn the user that the session will expire and allow the user to take action.
                $("#session-warning-modal").modal("show")
                .on("click", "#stay-logged-in", self.extendSession)
                .on("click", "#log-out", self.logout)
                .find("#remaining-time").text(Math.round(self.timeBeforeWarning / 60 / 1000));     
            },
            onbeforetimeout() {
                // By default this does nothing. Override this method to perform actions
                // (such as saving draft data) before the user is automatically logged out.
                // This may optionally return a jQuery Deferred object, in which case
                // ontimeout will be executed when the deferred is resolved or rejected.
            },
            ontimeout() {
                // Go to the timeout page.
                window.location.href = self.timeoutUrl;
            }
        },
        self = {},
        _warningTimeoutID,
        _expirationTimeoutID,
        // The time of the last ping to the server.
        _lastPingTime = 0;

    function extendSession() {
        // Extend the session expiration. Ping the server and reset the timers if
        // the minimum interval has passed since the last ping.
        var now = $.now(),
            timeSinceLastPing = now - _lastPingTime;

        if (timeSinceLastPing > self.minPingInterval) {
            _lastPingTime = now;
            _resetTimers();
            self.ping();
        }
    }

    function _resetTimers() {
        // Reset the session warning and session expiration timers.
        var warningTimeout = self.sessionLifetime - self.timeBeforeWarning;

        window.clearTimeout(_warningTimeoutID);
        window.clearTimeout(_expirationTimeoutID);
        _warningTimeoutID = window.setTimeout(self.onwarning, warningTimeout);
        _expirationTimeoutID = window.setTimeout(_onTimeout, self.sessionLifetime);
    }

    function _onTimeout() {
        // A wrapper that calls onbeforetimeout and ontimeout and supports asynchronous code.
        $.when(self.onbeforetimeout()).always(self.ontimeout);
    }

    // Add default variables and methods, user specified options, and non-overridable
    // public methods to the session monitor instance.
    $.extend(self, defaults, options, {
        extendSession: extendSession
    });
    // Set an event handler to extend the session upon user activity (e.g. mouseup).
    $(document).on(self.activityEvents, extendSession);
    // Start the timers and ping the server to ensure they are in sync with the backend session expiration.
    extendSession();

    return self;
};

sessMon = sessionMonitor();
window.sessMon = sessMon;
