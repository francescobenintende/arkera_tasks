import React, { Component } from 'react';
import './App.css';

import { FieldRouter } from "./FieldRouter";


class App extends Component {
    render() {
        return (
            <div className="App">
                <header className="App-header">
                    <FieldRouter/>
                </header>
            </div>
        );
    }
}

export default App;
