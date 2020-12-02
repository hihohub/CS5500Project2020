import React,{Component} from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';
import {LineChart,PieChart,ColumnChart} from 'react-chartkick';
import 'chart.js';

function replacer(key,value){
	if(key != undefined){
		return value;
	}
	return undefined;
}

function Parse(props){
	const json = JSON.stringify(props,replacer);
	const id = json.split('{"_id":');
	const data = id.map((s)=>
		s.split('"data":')[1]
	);
	const data_type = data.map((s)=>
		s.split('},')[0]
	);
	const sleep = data_type.filter(function(s){
		return s.includes("sleep");
	});
	const quantity = sleep.map((s)=>
		s.split('"quantity":')[1]
	);
	const clean = quantity.filter(function(s){
		return !s.includes("null");
	});
	const integers = clean.filter(function(s){
		return parseInt(s);
	});
	const listItems = clean.map((o)=>
		<li>{o}</li>
	);
	return (
		<ul>{listItems}</ul>	
	);
}

export default class Swagger extends React.Component {
	constructor(){
		super();
		this.state = {
			data:[],
			isLoading:true
		};
	}
	componentDidMount(){
		this.get_data_from_swagger("https://cs5500-healthcare.herokuapp.com/v1/cleanedData");
	}
	get_data_from_swagger(api){
		axios.get(api)
		.then(res=>{
			this.setState({
				isLoading:false,
				data:res.data
			});
		});
	}
	render(){
		return(
			<div>
			<h3>Sleep values from cleaned data</h3>
			{this.state.isLoading && 
				<p>LOADING...</p>
			}
			<Parse data={this.state.data}/>
			</div>
		);
	}
}
