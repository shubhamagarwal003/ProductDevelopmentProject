import Vue from 'vue/dist/vue.esm.js';


var riskFields = new Vue({
    el: '#risk',
    delimiters: ["[[", "]]"],
    data: {
        fields: {
            "text": [],
            "date":[],
            "number" : [],
            "enum":[],
        },
        name: '',
    },
})


function addField(field) {
    var tmp = {'name': field.name}
    if(field.options){
        tmp.options = field.options
    }
    riskFields.fields[field.dtype].push(tmp)
}
        
function getRiskField(riskId){
    fetch('/get/risk/'+riskId+'/')
    .then(function(data){
        return data.json()
    })
    .then(function(res) {
        riskFields.name = res.name;
        if(res.fields) {
            for(var i in res.fields) {
                addField(res.fields[i]);
            }
        }
    })
    .catch(function (error) {
        console.log(error.message);
    });
}

getRiskField('3');