const $ = q => document.querySelector(q);

const backgroundColor = [
    "rgb(255, 159, 64)", // ORANGE
    "rgb(255, 99, 132)", // RED
    "rgb(54, 162, 235)", // BLUE
    "rgb(75, 192, 192)", // GREEN
    "rgb(153, 102, 255)", // PURPLE
    "#f06595", // PINK
    "#fcc419" // YELLOW
];

function get(url) {
    return fetch(url).then(res => res.json());
}

{
    get("/number_of_videos_watched").then(res => $("#number_of_videos_watched").textContent = res);
    get("/total_watch_time").then(res => $("#total_watch_time").textContent = `${Math.round((res/3600) * 10) / 10} hours`);
    get("/number_of_ads_watched").then(res => $("#number_of_ads_watched").textContent = res);
    get("/total_ads_watch_time").then(res => $("#total_ads_watch_time").textContent = `${Math.round((res/3600) * 10) / 10} hours`);
    get("/most_watched_category").then(res => $("#most_watched_category").textContent = `${res[0]} (${res[1]} videos)`);
    get("/most_searched_word").then(res => $("#most_searched_word").textContent = `${res[0]} (${res[1]} times)`);
}

{
    let most_searched_words_chart;
    get("/most_searched_words").then(most_searched_words).then(chart => most_searched_words_chart = chart);
    function most_searched_words(res) {
        const labels = [], values = [];
        for (let p of res) {
            labels.push(p[0]);
            values.push(p[1]);
        }
        const data = {
            labels: labels,
            datasets: [
                {
                    label: "main dataset",
                    data: values,
                    backgroundColor: backgroundColor,
                }
            ]
        }
        const config = {
            type: 'pie',
            data: data,
            options: {
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                legend: {
                  position: 'top',
                  maxWidth: 600,
                },
                title: {
                  display: true,
                  text: 'Most Searched Words*'
                }
              }
            },
        };
        const ctx = document.getElementById('most_searched_words').getContext('2d');
        const myChart = new Chart(ctx, config);
        return myChart;
    }
    
    $("#most_searched_words_button").addEventListener("click", (e) => {
        const count = parseInt($("#most_searched_words_count").value);
        get(`/most_searched_words?count=${count}`).then(res => {
            const labels = [], values = [];
            for (let p of res) {
                labels.push(p[0]);
                values.push(p[1]);
            }
            most_searched_words_chart.data.labels = labels;
            most_searched_words_chart.data.datasets[0].data = values;
            most_searched_words_chart.update();
        });
    });
}

{
    let most_frequent_categories_chart;
    get("/most_frequent_categories").then(most_frequent_categories).then(chart => most_frequent_categories_chart = chart);
    function most_frequent_categories(res) {
        const labels = [], values = [];
        for (let p of res) {
            labels.push(p[0]);
            values.push(p[1]);
        }
        const data = {
            labels: labels,
            datasets: [
                {
                    label: "main dataset",
                    data: values,
                    backgroundColor: backgroundColor,
                }
            ]
        }
        const config = {
            type: 'pie',
            data: data,
            options: {
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                legend: {
                  position: 'top',
                  maxWidth: 600,
                },
                title: {
                  display: true,
                  text: 'Most Frequently Watched Categories*'
                }
              }
            },
        };
        const ctx = document.getElementById('most_frequent_categories').getContext('2d');
        const myChart = new Chart(ctx, config);
        return myChart;
    }
    
    $("#most_frequent_categories_button").addEventListener("click", (e) => {
        const count = parseInt($("#most_frequent_categories_count").value);
        get(`/most_frequent_categories?count=${count}`).then(res => {
            const labels = [], values = [];
            for (let p of res) {
                labels.push(p[0]);
                values.push(p[1]);
            }
            most_frequent_categories_chart.data.labels = labels;
            most_frequent_categories_chart.data.datasets[0].data = values;
            most_frequent_categories_chart.update();
        });
    });
    $("#most_frequent_categories_unit").addEventListener("click", (e) => {
        const count = parseInt($("#most_frequent_categories_count").value);
        const current_text = $("#most_frequent_categories_unit").textContent;
        let mode = "time";
        if (current_text == "unit: hours") {
            mode = "freq";
            $("#most_frequent_categories_unit").textContent = "unit: number of videos";
        } else {
            $("#most_frequent_categories_unit").textContent = "unit: hours";
        }
        get(`/most_frequent_categories?count=${count}&mode=${mode}`).then(res => {
            const labels = [], values = [];
            for (let p of res) {
                labels.push(p[0]);
                if (mode == "time") p[1] /= 60 * 60;
                values.push(Math.round(p[1] * 10) / 10);
            }
            most_frequent_categories_chart.data.labels = labels;
            most_frequent_categories_chart.data.datasets[0].data = values;
            most_frequent_categories_chart.update();
        });
    });
}

{
    let most_frequent_videos_chart;
    get("/most_frequent_videos").then(most_frequent_videos).then(chart => most_frequent_videos_chart = chart);
    function most_frequent_videos(res) {
        const labels = [], values = [];
        for (let p of res) {
            labels.push(p[0]);
            values.push(p[1]);
        }
        const data = {
            labels: labels,
            datasets: [
                {
                    label: "Video Watched Count",
                    data: values,
                    backgroundColor: backgroundColor,
                }
            ]
        };
        const config = {
            type: 'bar',
            data: data,
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        maxWidth: 600,
                    },
                    title: {
                        display: true,
                        text: 'Most Frequently Watched Videos'
                    }
                },
            },
        };
        const ctx = document.getElementById('most_frequent_videos').getContext('2d');
        const myChart = new Chart(ctx, config);
        return myChart;
    }
    
    $("#most_frequent_videos_button").addEventListener("click", (e) => {
        const count = parseInt($("#most_frequent_videos_count").value);
        get(`/most_frequent_videos?count=${count}`).then(res => {
            const labels = [], values = [];
            for (let p of res) {
                labels.push(p[0]);
                values.push(p[1]);
            }
            most_frequent_videos_chart.data.labels = labels;
            most_frequent_videos_chart.data.datasets[0].data = values;
            most_frequent_videos_chart.update();
        });
    });
}

{
    let most_popular_channels_chart;
    get("/most_popular_channels").then(most_popular_channels).then(chart => most_popular_channels_chart = chart);
    function most_popular_channels(res) {
        const labels = [], values = [];
        for (let p of res) {
            labels.push(p[0]);
            values.push(p[1]);
        }
        const data = {
            labels: labels,
            datasets: [
                {
                    label: "Subscriber Count",
                    data: values,
                    backgroundColor: backgroundColor,
                }
            ]
        };
        const config = {
            type: 'bar',
            data: data,
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'top',
                        maxWidth: 600,
                    },
                    title: {
                        display: true,
                        text: 'Most Popular Subscriptions'
                    }
                },
            },
        };
        const ctx = document.getElementById('most_popular_channels').getContext('2d');
        const myChart = new Chart(ctx, config);
        return myChart;
    }
    
    $("#most_popular_channels_button").addEventListener("click", (e) => {
        const count = parseInt($("#most_popular_channels_count").value);
        get(`/most_popular_channels?count=${count}`).then(res => {
            const labels = [], values = [];
            for (let p of res) {
                labels.push(p[0]);
                values.push(p[1]);
            }
            most_popular_channels_chart.data.labels = labels;
            most_popular_channels_chart.data.datasets[0].data = values;
            most_popular_channels_chart.update();
        });
    });
}

{
    let most_frequent_channels_chart;
    get("/most_frequent_channels").then(most_frequent_channels).then(chart => most_frequent_channels_chart = chart);
    function most_frequent_channels(res) {
        const labels = [], values = [];
        for (let p of res) {
            labels.push(p[0]);
            values.push(p[1]);
        }
        const data = {
            labels: labels,
            datasets: [
                {
                    label: "Videos Watched",
                    data: values,
                    backgroundColor: backgroundColor,
                }
            ]
        }
        const config = {
            type: 'bar',
            data: data,
            options: {
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                legend: {
                  position: 'top',
                  maxWidth: 600,
                },
                title: {
                  display: true,
                  text: 'Most Frequently Watched Channels*'
                }
              }
            },
        };
        const ctx = document.getElementById('most_frequent_channels').getContext('2d');
        const myChart = new Chart(ctx, config);
        return myChart;
    }
    
    $("#most_frequent_channels_button").addEventListener("click", (e) => {
        const count = parseInt($("#most_frequent_channels_count").value);
        get(`/most_frequent_channels?count=${count}`).then(res => {
            const labels = [], values = [];
            for (let p of res) {
                labels.push(p[0]);
                values.push(p[1]);
            }
            most_frequent_channels_chart.data.labels = labels;
            most_frequent_channels_chart.data.datasets[0].data = values;
            most_frequent_channels_chart.update();
        });
    });
    $("#most_frequent_channels_unit").addEventListener("click", (e) => {
        const count = parseInt($("#most_frequent_channels_count").value);
        const current_text = $("#most_frequent_channels_unit").textContent;
        let mode = "time";
        if (current_text == "unit: hours") {
            mode = "freq";
            $("#most_frequent_channels_unit").textContent = "unit: number of videos";
        } else {
            $("#most_frequent_channels_unit").textContent = "unit: hours";
        }
        get(`/most_frequent_channels?count=${count}&mode=${mode}`).then(res => {
            const labels = [], values = [];
            for (let p of res) {
                labels.push(p[0]);
                if (mode == "time") p[1] /= 60 * 60;
                values.push(Math.round(p[1] * 10) / 10);
            }
            most_frequent_channels_chart.data.labels = labels;
            most_frequent_channels_chart.data.datasets[0].data = values;
            most_frequent_channels_chart.update();
        });
    });
}
