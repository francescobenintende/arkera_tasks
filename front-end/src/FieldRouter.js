import React, { Component } from 'react';

import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import { TablePage } from './TablePage';

import { getCitiesData } from './data_fectcher';



function pathify(name) {
    if (name === '#') {
        return 'id';
    }
    return name.toLowerCase().replace(' ', '-');
}


export class FieldRouter extends Component {

    constructor(props) {
        super(props);

        this.state = {
            headers: [],
            cities: []
        };

        this.updateTableData = this.updateTableData.bind(this);

        getCitiesData((headers, cities) => {
            this.updateTableData(headers, cities);
        });
    }

    updateTableData(headers, cities) {
        this.setState({
            headers: headers,
            cities: cities
        });
    }

    createRoute(header) {
        const accessor = header['accessor'];
        const path = pathify(accessor);

        return (
            <Route exact={true} path={`/${path}`} key={path}>
                <TablePage
                    headers={this.state.headers}
                    cities={this.state.cities}
                    currentlySelectedHeader={accessor}
                />
            </Route>
        );
    }

    render() {
        return (
            <Router>
                <Switch>
                    {this.state.headers.map((header) => this.createRoute(header))}
                    <Route path="*" render={() => (<TablePage
                        headers={this.state.headers}
                        cities={this.state.cities}
                        currentlySelectedHeader={'#'}
                    />)} />
                </Switch>
            </Router>
        );
    }

}