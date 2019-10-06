/* Copyright 2019, Greatery Development Team
   Distributed under the terms of the Apache License 2.0
*/
import React from 'react';

class EntryForm extends React.Component {
	render() {
		return (
			<form method="post" action={this.props.url}>
			<input type="hidden" name="_xsrf" value={this.props.xsrf}/>
				<h2>Add an Entry</h2>
				<div className="form-group">
					<label>
                        Kind of item: Ingredient or Meal
						<input name="name" type="text" className="form-control" placeholder="..." />
					</label>
				</div>
				<div className="form-group">
					<label>
                        Description of item:
						<textarea name="desc" className="form-control" placeholder="..." />
					</label>
				</div>
				<div className="text-right">
					<button type="reset" className="btn btn-default">Reset</button>
					<button type="submit" className="btn btn-primary">Submit</button>
				</div>
			</form>
		);
	}
}

export default EntryForm;
