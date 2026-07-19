document.addEventListener("DOMContentLoaded", () => {
    let tickets = [];

    // Load tickets from backend
    fetch("/api/tickets")
        .then(res => res.json())
        .then(data => {
            tickets = data;
            const selector = document.getElementById("ticket-selector");
            tickets.forEach((t, i) => {
                const opt = document.createElement("option");
                opt.value = i;
                opt.textContent = `[${t.type.toUpperCase()}] ${t.text.substring(0, 40)}...`;
                selector.appendChild(opt);
            });
        });

    document.getElementById("ticket-selector").addEventListener("change", (e) => {
        if(e.target.value !== "") {
            document.getElementById("ticket-input").value = tickets[e.target.value].text;
        }
    });

    document.getElementById("btn-safe").addEventListener("click", () => {
        const safeTickets = tickets.filter(t => t.type === "safe");
        if(safeTickets.length > 0) {
            const randomSafe = safeTickets[Math.floor(Math.random() * safeTickets.length)];
            document.getElementById("ticket-input").value = randomSafe.text;
        }
    });

    document.getElementById("btn-attack").addEventListener("click", () => {
        const maliciousTickets = tickets.filter(t => t.type === "malicious");
        if(maliciousTickets.length > 0) {
            const randomMalicious = maliciousTickets[Math.floor(Math.random() * maliciousTickets.length)];
            document.getElementById("ticket-input").value = randomMalicious.text;
        }
    });

    document.getElementById("btn-process").addEventListener("click", () => {
        const text = document.getElementById("ticket-input").value;
        if(!text) return;

        document.getElementById("processing-indicator").classList.remove("hidden");
        document.getElementById("results-container").classList.add("hidden");
        document.getElementById("btn-process").disabled = true;

        fetch("/api/process", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ ticket_text: text })
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById("processing-indicator").classList.add("hidden");
            document.getElementById("results-container").classList.remove("hidden");
            document.getElementById("btn-process").disabled = false;

            // Populate Agent Box
            document.getElementById("res-action").textContent = data.agent.action;
            document.getElementById("res-agent-reason").textContent = data.agent.reason;

            // Populate Rule Box
            const ruleRes = document.getElementById("res-rule");
            ruleRes.textContent = data.rules.decision;
            ruleRes.className = data.rules.decision === "ALLOW" ? "status-allow" : "status-block";

            // Populate Judge Box
            const judgeChecksDiv = document.getElementById("res-judge-checks");
            if (data.judge.decision === "BLOCK") {
                judgeChecksDiv.innerHTML = `
                    <div class="status-block" style="margin: 4px 0;">✗ Prompt Injection Detected</div>
                    <div class="status-block" style="margin: 4px 0;">✗ Unauthorized Request</div>
                    <div class="status-block" style="margin: 4px 0;">✗ Violates Agent Spec</div>
                `;
            } else {
                judgeChecksDiv.innerHTML = `
                    <div class="status-allow" style="margin: 4px 0;">✓ Clean Request</div>
                    <div class="status-allow" style="margin: 4px 0;">✓ Authorized Action</div>
                    <div class="status-allow" style="margin: 4px 0;">✓ Complies with Agent Spec</div>
                `;
            }
            
            const riskRes = document.getElementById("res-risk");
            riskRes.textContent = data.final.final_risk;
            riskRes.className = "";
            if(data.final.final_risk === "CRITICAL" || data.final.final_risk === "HIGH") riskRes.className = "status-block";

            // Populate Final Box
            const finalBox = document.getElementById("final-decision-box");
            const finalH1 = document.getElementById("res-final");
            const finalReason = document.getElementById("res-final-reason");
            
            if(data.final.final_decision === "ALLOW") {
                finalH1.textContent = "✅ ALLOWED";
                finalBox.className = "result-box final-box final-allow";
                finalH1.className = "status-allow";
                finalReason.innerHTML = data.final.reason;
            } else {
                finalH1.textContent = "🛑 AGENT FROZEN";
                finalBox.className = "result-box final-box final-block";
                finalH1.className = "status-block";
                
                finalReason.innerHTML = `
                    <div style="text-align: left; margin-top: 15px; font-size: 14px; line-height: 1.6;">
                        <strong>Detected Threat:</strong> ${data.final.reason}<br><br>
                        The IT Support Agent is only allowed to:
                        <ul style="margin: 5px 0 15px 20px; padding: 0;">
                            <li>Reset Password</li>
                            <li>Unlock Account</li>
                            <li>Check Status</li>
                        </ul>
                        <strong>No action was executed.</strong> The request has been added to the quarantine log.
                    </div>
                `;
            }

            loadLogs();
        })
        .catch(err => {
            console.error(err);
            document.getElementById("processing-indicator").classList.add("hidden");
            document.getElementById("btn-process").disabled = false;
            alert("Error processing ticket. Ensure backend is running and API key is set.");
        });
    });

    document.getElementById("btn-refresh-logs").addEventListener("click", loadLogs);

    function loadLogs() {
        fetch("/api/logs/audit")
            .then(res => res.json())
            .then(logs => {
                const container = document.getElementById("log-container");
                container.innerHTML = "";
                // Reverse to show newest first
                logs.reverse().forEach(log => {
                    const div = document.createElement("div");
                    
                    if (log.decision === "ALLOW") {
                        div.className = "log-item log-allow";
                    } else {
                        div.className = "log-item log-block";
                    }
                    
                    const date = new Date(log.timestamp).toLocaleString();
                    div.innerHTML = `
                        <div class="log-timestamp">${date}</div>
                        <strong>Prompt:</strong> ${log.ticket}<br><br>
                        <strong>Action:</strong> ${log.detected_action} <span style="float:right; font-weight:bold; color: ${log.decision === 'ALLOW' ? 'var(--success)' : 'var(--danger)'}">${log.decision}</span><br>
                        <strong>Reason:</strong> ${log.reason}
                    `;
                    container.appendChild(div);
                });
            })
            .catch(err => console.error(err));
    }

    loadLogs();
    
    // Modal Logic
    const modal = document.getElementById("spec-modal");
    document.getElementById("btn-view-spec").addEventListener("click", () => {
        modal.classList.remove("hidden");
    });
    document.getElementById("close-modal").addEventListener("click", () => {
        modal.classList.add("hidden");
    });
    window.addEventListener("click", (e) => {
        if(e.target === modal) {
            modal.classList.add("hidden");
        }
    });
});
