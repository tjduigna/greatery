/* Copyright 2019, Greatery Development Team
   Distributed under the terms of the Apache License 2.0
*/
import React from 'react';
import Entry from './entry.jsx';

class EntryList extends React.Component {
	render() {
		if (!this.props.entries.length) {
			return null;
		}
		var entryNodes = this.props.entries.map((entry, index) => {
			return <Entry name={entry.name} desc={entry.desc} key={index} />;
		});
		return (
			<div>
				<h2>Entries</h2>
				{entryNodes}
			</div>
		);
	}
}

export default EntryList;

