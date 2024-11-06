function turn_off_loader() {
    document.getElementById('loader').classList.add('d-none');
    document.getElementById('spinner').classList.add('d-none');
    document.body.style.overflow = 'auto';
}

const resultSettings = {
    'win': {
      'placeholder': 'Победа',
      'result_class': 'bg-success'
    },
    'loose': {
      'placeholder': 'Поражение',
      'result_class': 'bg-danger'
    },
    'opened': {
      'placeholder': 'В процессе',
      'result_class': 'bg-primary'
    },
    'failed': {
      'placeholder': 'Ошибка записи',
      'result_class': 'bg-dark'
    },
}

function format_hero_name(heroName) {
    return heroName.replace('npc_dota_hero_', '')
}

function format_utc_to_mmss(d) {
    var minutes = Math.floor(Math.abs(d) / 60);
    var seconds = Math.abs(d) % 60;
    if (d < 0) {
        minus = '-'
    } else {
        minus = ''
    }
    return minus + minutes + ":" + (seconds < 10 ? "0" : "") + seconds;
}

function format_datetime(input_datetime) {
    let datetime = new Date(input_datetime);
    let formattedDatetime = datetime.toLocaleString("ru-RU", {
      year: "2-digit",
      month: "2-digit",
      day: "2-digit",
      hour: "2-digit",
      minute: "2-digit",
    }).replace(",", "");
    return formattedDatetime
  }

function get_result_html_for_table(game_result) {
    let placeholder = resultSettings[game_result]['placeholder']
    let result_class = resultSettings[game_result]['result_class']
    let html_str = "<div class='status-badge " + result_class + "'>"
    html_str += placeholder
    html_str += "</div>"
    return html_str
  }

  function set_settings_for_chart(chart, id) {
    chart.container(id);
    chart.draw();
    chart.background().fill("");
    chart.title().fontColor("white");
    
    chart.yAxis().orientation("right");
    chart.yAxis().minorTicks().enabled(true);
    chart.xAxis().minorTicks().enabled(false);
    chart.xAxis().ticks().enabled(false)

    chart.legend(true);
    chart.legend().fontColor("white");
    chart.legend().position("left");
    chart.legend().align("top");
    chart.legend().positionMode("inside");
    chart.legend().itemsLayout("vertical-expandable");
    chart.legend().maxWidth("80%");
}
