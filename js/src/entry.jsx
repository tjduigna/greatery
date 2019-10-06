/* Copyright 2019, Greatery Development Team
   Distributed under the terms of the Apache License 2.0
*/
import React from 'react';

class Entry extends React.Component {
	render() {
		return (
			<div>
				<h3>{this.props.name}</h3>
				{this.props.desc}
			</div>
		);
	}
}

export default Entry;

