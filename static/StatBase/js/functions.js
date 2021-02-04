$(document).ready(function(){	 
  // comparison functions
  var openCompareButton = $('#pps-button-first, .searchbox-compare');
  var submitCompareIcon = $('.searchbox-compare-submit');
  var inputCompareBox = $('.searchbox-compare-input');
  var searchBoxCompare = $('.searchbox-compare');
  var isOpenCompare = false;

  $(".top-results-row, .top-results-row-even, .search-result-row").click(function() {
    window.location = $(this).data("url");
  });

  openCompareButton.click(function(){
    if(isOpenCompare == false){
      searchBoxCompare.addClass('searchbox-compare-open');
      $('.searchbox-compare-icon, .searchbox-compare-submit').addClass('clicked');
      inputCompareBox.focus();
      isOpenCompare = true;
    } 
    else {
      searchBoxCompare.removeClass('searchbox-compare-open');
      $('.searchbox-compare-icon, .searchbox-compare-submit').removeClass('clicked');
      inputCompareBox.focusout();
      isOpenCompare = false;
    }
  }); 
  
  openCompareButton.mouseup(function(){
    return false;
  });
  
  $(document).mouseup(function(){
    if(isOpenCompare == true){
      $('.searchbox-compare-icon').css('display','block');
      submitCompareIcon.click();
    }
  });
// datatable functions
  $('#best-goals-90-table').DataTable();
  var swiper = new Swiper('.swiper-container', {
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
  });
  var submitIcon = $('.searchbox-icon');
  var inputBox = $('.searchbox-input');
  var searchBox = $('.searchbox');
  var isOpen = false;
  submitIcon.click(function(){
    if(isOpen == false){
      searchBox.addClass('searchbox-open');
      $('.searchbox-icon').addClass('clicked');
      $('.searchbox-submit').addClass('clicked');
      inputBox.focus();
      isOpen = true;
    } 
    else {
      searchBox.removeClass('searchbox-open');
      $('.searchbox-icon').removeClass('clicked');
      $('.searchbox-submit').removeClass('clicked');
      inputBox.focusout();
      isOpen = false;
    }
  });  
  submitIcon.mouseup(function(){
    return false;
  });
  searchBox.mouseup(function(){
    return false;
  });
  $(document).mouseup(function(){
    if(isOpen == true){
      $('.searchbox-icon').css('display','block');
      submitIcon.click();
    }
  });
});
function buttonUp(){
  var inputVal = $('.searchbox-input').val();
  inputVal = $.trim(inputVal).length;
  if( inputVal !== 0){
      $('.searchbox-icon').css('display','none');
  } else {
      $('.searchbox-input').val('');
      $('.searchbox-icon').css('display','block');
  }
}

function buttonCompareUp(){
  var inputVal = $('.searchbox-compare-input').val();
  inputVal = $.trim(inputVal).length;
  }

document.addEventListener("DOMContentLoaded", function(event) {
  // stats_tables
  tippy('#tt_seasons',  {
    content: "Number of player's career seasons",
    placement: "top",
    delay: 200
  });
  
  tippy('#tt_cc', {
    content: "Canadian classification points: goals + assists",
    placement: "top",
    delay: 200
  });
  tippy('#tt_yc90', {
    content: "Yellow cards/90 minutes",
    placement: "top",
    delay: 200
  });
  tippy('#tt_sb_aggression_index', {
    content: "The lower the value, the more aggressive the player is",
    placement: "top",
    delay: 200
  });
  // db_update
  tippy('#tt_transfer_player', {
    content: "Use this function if access to TM's database is not denied",
    placement: "bottom",
    delay: 100
  });
  tippy('#tt_transfer_data', {
    content: "Transfer only one data at the time",
    placement: "bottom",
    delay: 100
  });
  tippy('#tt_transfer_leagues', {
    content: "Transfer all leagues that existing in db players was playing for",
    placement: "bottom",
    delay: 100
  });
});

// C H A R T S

function player_season_goal_chart(player_obj){ 
  var player = sanitizePythObjs(player_obj);
  var ctx = document.getElementById('myChartYu').getContext('2d');

  var player_season_stats_chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [],
      datasets: [{
        label: 'Total season goals',
        backgroundColor: 'rgba(0, 0, 0, 0',
        borderColor: '#767c87',
        lineTension: 0,
        data: [],
        pointStyle: [],
      }, 
      {
        label: 'Total season assists',
        backgroundColor: 'rgba(0, 0, 0, 0)',
        borderColor: '#b0b6bf',
        lineTension: 0,
        data: [],
        pointStyle: [],
      }, 
      {
        label: 'Total SB index',
        backgroundColor: 'rgba(0, 0, 0, 0)',
        borderColor: '#e4e7ed',
        lineTension: 0,
        data: [],
        pointStyle: [],
      },
    ]
    },
    options: {}
});
  for (var season in player['detailed_stats']['seasons']) {
    addLabel(player_season_stats_chart, player['detailed_stats']['seasons'][season]);
  }
  for (var goal in player['detailed_stats']['goals']) {
    addData(player_season_stats_chart, player['detailed_stats']['goals'][goal], 0);
  }
  for (var assist in player['detailed_stats']['assists']) {
    addData(player_season_stats_chart, player['detailed_stats']['assists'][assist], 1);
  }
  for (var sb_index in player['season_competition_stats']['sb_index_by_season']) {
    addData(player_season_stats_chart, player['season_competition_stats']['sb_index_by_season'][sb_index], 2);
  }

  for (var club_img_idx in player['detailed_stats']['club_img']) {
    var club_image = new Image();
    club_image.src = player['detailed_stats']['club_img'][club_img_idx];
    addClubImgs(player_season_stats_chart, club_image, 0);
    addClubImgs(player_season_stats_chart, club_image, 1);
    addClubImgs(player_season_stats_chart, club_image, 2);
  }
}


function generate_player_comparison_chart(player_1_obj, player_2_obj){   
  var p1 = sanitizePythObjs(player_1_obj);
  var p2 = sanitizePythObjs(player_2_obj);
  common_seasons = get_both_career_seasons(p1['detailed_stats'], p2['detailed_stats']);
  addNecessaryZeros(p1, p2);

  var ctx = document.getElementById('player_comp_chart').getContext('2d');
  var player_comparison_chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [],
      datasets: [{
        label: p1['full_name'] + "'s total season goals",
        backgroundColor: 'rgba(0, 0, 0, 0',
        borderColor: '#FF0000',
        lineTension: 0,
        data: [],
        pointStyle: [],
        hidden: true,
      }, 
      {
        label: p1['full_name'] + "'s total season assists",
        backgroundColor: 'rgba(0, 0, 0, 0',
        borderColor: '#CE5454',
        lineTension: 0,
        data: [],
        pointStyle: [],
        hidden: true,
      }, 
      {
        label: p1['full_name'] + "'s total season goals + assists",
        backgroundColor: 'rgba(0, 0, 0, 0',
        borderColor: '#9A0B0B',
        lineTension: 0,
        data: [],
        pointStyle: [],
      
      },
      {
        label: p1['full_name'] + "'s total season SB index",
        backgroundColor: 'rgba(0, 0, 0, 0',
        borderColor: '#780505',
        lineTension: 0,
        data: [],
        pointStyle: [],
        hidden: true,
      },
      {
        label: p2['full_name'] + "'s total season goals",
        backgroundColor: 'rgba(0, 0, 0, 0',
        borderColor: '#0080FF',
        lineTension: 0,
        data: [],
        pointStyle: [],
        hidden: true,
      }, 
      {
        label: p2['full_name'] + "'s total season assists",
        backgroundColor: 'rgba(0, 0, 0, 0',
        borderColor: '#3C7FC2',
        lineTension: 0,
        data: [],
        pointStyle: [],
        hidden: true,
      }, 
      {
        label: p2['full_name'] + "'s total season goals + assists",
        backgroundColor: 'rgba(0, 0, 0, 0',
        borderColor: '#074482',
        lineTension: 0,
        data: [],
        pointStyle: [],

      }, 
      {
      label: p2['full_name'] + "'s total season SB index",
      backgroundColor: 'rgba(0, 0, 0, 0',
      borderColor: '#06325e',
      lineTension: 0,
      data: [],
      pointStyle: [],
      hidden: true,
      }
    ]
    },
    options: {
      legend: {
        position: 'top'}
    }
  });
  for (var season in common_seasons) {
    addLabel(player_comparison_chart, common_seasons[season]);
  }
  for (var season_idx in p1['detailed_stats']['goals']){
    addData(player_comparison_chart, p1['detailed_stats']['goals'][season_idx], 0)
  }
  for (var season_idx in p1['detailed_stats']['assists']){
    addData(player_comparison_chart, p1['detailed_stats']['assists'][season_idx], 1)
  }
  for (var season_idx in p1['detailed_stats']['cc']){
    addData(player_comparison_chart, p1['detailed_stats']['cc'][season_idx], 2)
  }
  for (var season_idx in p1['season_competition_stats']['sb_index_by_season']){
    addData(player_comparison_chart, p1['season_competition_stats']['sb_index_by_season'][season_idx], 3)
  }
  for (var season_idx in p2['detailed_stats']['goals']){
    addData(player_comparison_chart, p2['detailed_stats']['goals'][season_idx], 4)
  }
  for (var season_idx in p2['detailed_stats']['assists']){
    addData(player_comparison_chart, p2['detailed_stats']['assists'][season_idx], 5)
  }
  for (var season_idx in p2['detailed_stats']['cc']){
    addData(player_comparison_chart, p2['detailed_stats']['cc'][season_idx], 6)
  }
  for (var season_idx in p2['season_competition_stats']['sb_index_by_season']){
    addData(player_comparison_chart, p2['season_competition_stats']['sb_index_by_season'][season_idx], 7)
  }
  for (var club_img_idx in p1['detailed_stats']['club_img']) {
    var club_image = new Image();
    club_image.src = p1['detailed_stats']['club_img'][club_img_idx];
    addClubImgs(player_comparison_chart, club_image, 0);
    addClubImgs(player_comparison_chart, club_image, 1);
    addClubImgs(player_comparison_chart, club_image, 2);
    addClubImgs(player_comparison_chart, club_image, 3);
  }
  for (var club_img_idx in p2['detailed_stats']['club_img']) {
    var club_image = new Image();
    club_image.src = p2['detailed_stats']['club_img'][club_img_idx];
    addClubImgs(player_comparison_chart, club_image, 4);
    addClubImgs(player_comparison_chart, club_image, 5);
    addClubImgs(player_comparison_chart, club_image, 6);
    addClubImgs(player_comparison_chart, club_image, 7);
  }
}


function generate_goal_type_chart(player_obj){ 
  var player = sanitizePythObjs(player_obj);
  var goals_types_keys = Object.keys(player['detailed_stats']['goals_types']);
  
  var ctx = document.getElementById('goal_type_chart').getContext('2d');
  var goal_type_chartx = new Chart(ctx, {
    type: 'radar',
    data: {
      labels: ["Right-footed shot", "Left-footed shot", "Header", "Penalty", "Direct free kick", "Long distance kick", "Tap-in", "Other", "Unknown"],
      datasets: [{
        label: "",
        backgroundColor: "rgba(200,0,0,0.2)",
        data: []
      }, 
    ]
    },
    options: {
      legend: {
        display: false}
      }
  });
  for (var key_idx in goals_types_keys){
    var key_name = goals_types_keys[key_idx]
    addData(goal_type_chartx, player['detailed_stats']['goals_types'][key_name], 0)
    }
  }


function generate_goal_type_comparison_chart(p1_dict, p2_dict){ 
  var p1 = sanitizePythObjs(p1_dict);
  var p2 = sanitizePythObjs(p2_dict);
  var ctx = document.getElementById('goal_type_comparison_chart').getContext('2d');
  var goal_type_comparison_chartx = new Chart(ctx, {
    type: 'radar',
    data: {
      labels: ["Right-footed shot", "Left-footed shot", "Header", "Penalty", "Direct free kick", "Long distance kick", "Tap-in", "Other", "Unknown"],
      datasets: [{
        label: p1['full_name'],
        backgroundColor: "rgba(255, 0, 0, 0.301)",
        data: []
      }, 
      {
        label: p2['full_name'],
        backgroundColor: "rgba(0, 47, 255, 0.301)",
        data: []
      }, 
    ]
  },
  options: {
    legend: {
      display: true}
    }
  });
  for (var key_idx in Object.keys(p1['detailed_stats']['goals_types'])){
    var key_name = Object.keys(p1['detailed_stats']['goals_types'])[key_idx]
    addData(goal_type_comparison_chartx, p1['detailed_stats']['goals_types'][key_name], 0)
  }
  for (var key_idx in Object.keys(p2['detailed_stats']['goals_types'])){
    var key_name = Object.keys(p2['detailed_stats']['goals_types'])[key_idx]
    addData(goal_type_comparison_chartx, p2['detailed_stats']['goals_types'][key_name], 1)
  }
}

// C H A R T   H E L P E R S

function addLabel(chart_name, new_label) {
  chart_name.data.labels.push(new_label); 
  chart_name.update();
}
function addData(chart_name, new_data_list, dataset_num) {
  chart_name.data.datasets[dataset_num].data.push(new_data_list); 
  chart_name.update();
}
function addClubImgs(chart_name, new_club_imgs_list, dataset_num) {
  chart_name.data.datasets[dataset_num].pointStyle.push(new_club_imgs_list); 
  chart_name.update();
}
function get_all_players_names(players_names_id_dict){
  var players_names_id_dict_raw = decodeHtml(players_names_id_dict).replace(/'/g, "\"").replace(/None/g, "\"None\"");
  var players_names_id_dict_parsed = JSON.parse(players_names_id_dict_raw);
  var players_names_list = Object.keys(players_names_id_dict_parsed);
  $( function() {
    $( "#compare-players" ).autocomplete({
      source: players_names_list,
      select: function( event, ui ) {
      },
      change: function( event, ui ) {
        if ( !ui.item ) {
              alert("You have to select one of the players from drop-down list!")
              $("#compare-players").val("");
              window.location.reload(true);
        }
      }
    });
  });
}

function get_both_career_seasons(player_1_stats_dict, player_2_stats_dict){
  var common_seasons = player_1_stats_dict['seasons'].slice(0);
  for (season_idx in player_2_stats_dict['seasons']){
    if (!(player_1_stats_dict['seasons'].includes(player_2_stats_dict['seasons'][season_idx]))) {
      common_seasons.push(player_2_stats_dict['seasons'][season_idx]);
    }
  }
  common_seasons.sort();
  return common_seasons;
};


// SINCE TWO PLAYERS CAN HAVE LONGER OR SHORTER CAREERS, I NEED TO FILL THE DATA WITH NECESSARY ZEROS
function addNecessaryZeros(p1, p2){
  if (p1['detailed_stats']['seasons'][0] < p2['detailed_stats']['seasons'][0]){ 
      var sooner = p1;
      var later = p2;
  } else {
      var sooner = p2;
      var later = p1;
  }
  var dif = later['detailed_stats']['seasons'][0] - sooner['detailed_stats']['seasons'][0];
  for (key_idx in (Object.keys(later['detailed_stats']))){
    var key_name = (Object.keys(later['detailed_stats'])[key_idx])
    for (i = 0; i < dif; i++) {
      
      if (Array.isArray(later['detailed_stats'][key_name])){
        later['detailed_stats'][key_name].unshift(''); 
      }
      
    }
  }
  // just for sb index
  for (i = 0; i < dif; i++) {
    later['season_competition_stats']['sb_index_by_season'].unshift(''); 
  }
  
}

  function generate_stats_comparison_radar(p1_obj, p2_obj){ 
    var p1 = sanitizePythObjs(p1_obj);
    var p2 = sanitizePythObjs(p2_obj);
    var ctx = document.getElementById('stats_comparison_radar').getContext('2d');
    var stats_comparison_radarx = new Chart(ctx, {
        type: 'radar',
        data: {
          labels: ["Goals/90", "Assists/90", "Canadian points/90"],
          datasets: [{
            label: p1['full_name'],
            backgroundColor: "rgba(255, 0, 0, 0.301)",
            data: [p1['goals_90'], p1['assists_90'], p1['cc_90']]
          }, 
          {
            label: p2['full_name'],
            backgroundColor: "rgba(0, 47, 255, 0.301)",
            data: [p2['goals_90'], p2['assists_90'], p2['cc_90']]
          }, 
        ]
      },
      options: {
        legend: {
          display: true}
        }
    });
  }

// OTHER HELPERS

function decodeEntities(encodedString) {
  var translate_re = /&(nbsp|amp|quot|lt|gt);/g;
  var translate = {
      "nbsp":" ",
      "amp" : "&",
      "quot": "\"",
      "lt"  : "<",
      "gt"  : ">"
  };
  return encodedString.replace(translate_re, function(match, entity) {
      return translate[entity];
  }).replace(/&#(\d+);/gi, function(match, numStr) {
      var num = parseInt(numStr, 10);
      return String.fromCharCode(num);
  });
}

function sanitizePythObjs(object){
  //alert(JSON.parse(decodeHtml(object).replace(/'/g, "\"").replace(/\"{\"/g, "{\"").replace(/}\"/g, "}").replace(/\"{\"/g, "{\"").replace(/}\"}\"/g, "}}")));
  return JSON.parse(decodeHtml(object).replace(/'/g, "\"").replace(/\"{\"/g, "{\"").replace(/}\"/g, "}").replace(/\"{\"/g, "{\"").replace(/}\"}\"/g, "}}"));
  //.replace(/\"{/g, "{")
  //.replace(/}\"}\"}\"/g, "}}}")
}
function decodeHtml(html) {
  var txt = document.createElement("textarea");
  txt.innerHTML = html;
  return txt.value;
}