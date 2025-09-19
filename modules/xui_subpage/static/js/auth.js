(function () {
    const params = new URLSearchParams(window.location.search);
    const direct = params.get('url');
    if (direct) {
        window.location.replace(direct);
        return;
    }

    const tg = window.Telegram && window.Telegram.WebApp;
    const insideTelegram =
        !!(tg && ((tg.initData && tg.initData.length > 0) ||
                  (tg.initDataUnsafe && (tg.initDataUnsafe.query_id || tg.initDataUnsafe.user))));

    if (insideTelegram) {
        var initData = (window.Telegram && window.Telegram.WebApp && window.Telegram.WebApp.initData) || '';
        try {
            fetch((window.BASE_PATH || '/connect/') + 'auth/start?init_data=' + encodeURIComponent(initData), {
                method: 'POST',
                credentials: 'include'
            })
            .catch(function(){})
            .finally(function(){
                document.documentElement.classList.add('tg');
            });
        } catch (e) {
            document.documentElement.classList.add('tg');
        }
        return;
    }

    window.location.replace('https://t.me/{{USERNAME_BOT}}?start=start');
})();