$(function () {
    var chart;
    $(document).ready(function() {

        $.getJSON(
            '/api/group/habits/',
            {
                name: 'statins'
            },
            function(data, status, xhr){
                console.log(data);
                var categories, series;

                categories = _.map(data[0].habit, function(x){return x.period});
                series = _.map(data,
                               function(x){
                                   series = {name: x.name, patent:x.patent, data:
                                             _.map(x.habit, function(y){
                                                 return y.total
                                             })};
                                   if(x.patent){
                                       var which = categories.indexOf(parseInt(x.patent, 10));
                                       var level = series.data[which];
                                       series.data[which] = {y: level, marker: {
                                           symbol: 'url(http://www.highcharts.com/demo/gfx/sun.png)'
                                       }}
                                   };
                                   return series
                               });

                console.log(series);

                chart = new Highcharts.Chart({
                    chart: {
                        renderTo: 'container',
                        type: 'line',
                        marginRight: 130,
                        marginBottom: 25
                    },
                    title: {
                        text: 'Monthly UK Statins with Patent expiry',
                        x: -20 //center
                    },
                    subtitle: {
                        text: 'Source: ic.nhs.uk',
                        x: -20
                    },
                    xAxis: {
                        categories: categories
                    },
                    yAxis: {
                        title: {
                            text: 'Number of prescriptions'
                        },
                        plotLines: [{
                            value: 0,
                            width: 1,
                            color: '#808080'
                        }]
                    },
                    tooltip: {
                        formatter: function() {
                            if (this.series.patent){
                                patent = 'Patent expires ' + this.series.patent;
                            }else{
                                patent = '';
                            }
                            return '<b>'+ this.series.name +'</b><br/>'+
                                this.x +': '+ this.y +' prescriptions' + '\n' + patent;
                        }
                    },
                    legend: {
                        layout: 'vertical',
                        align: 'right',
                        verticalAlign: 'top',
                        x: -10,
                        y: 100,
                        borderWidth: 0
                    },
                    series: series

                });
            });

            }
        )

});
