function toggleAlert() {
    fetch("/toggle_alert", { method: "POST" })
        .then(res => res.json())
        .then(data => {
            const video = document.getElementById("videoFeed");
            const btn = document.getElementById("alertBtn");
            const status = document.getElementById("alertStatus");

            if (data.alert) {
                video.classList.remove("alert-off");
                video.classList.add("alert-on");
                btn.innerText = "🔔 Alert ON";
                status.innerText = "Alert System: ACTIVE";
                status.style.color = "red";
            } else {
                video.classList.remove("alert-on");
                video.classList.add("alert-off");
                btn.innerText = "🔕 Alert OFF";
                status.innerText = "Alert System: DISABLED";
                status.style.color = "lime";
            }
        });
}
