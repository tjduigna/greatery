/* Copyright 2019, Greatery Development Team
   Distributed under the terms of the Apache License 2.0
*/
import React from 'react'
import EntryList from './entrylist.jsx'
import EntryForm from './entryform.jsx'
import Button from '@material-ui/core/Button'

import Select from 'react-select'


class App extends React.Component {
	render() {
		return (
			<div>
                <Button variant="contained" color="primary">
                    Hello World
                </Button>
                <Select options={this.props.kinds_of_entries} />
				<EntryForm url={this.props.url} xsrf={this.props.xsrf}/>
				<EntryList entries={this.props.entries} />
			</div>
		);
	}
}

export default App;
