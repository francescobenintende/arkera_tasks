import React from 'react';
import ReactTable from 'react-table';
import "react-table/react-table.css";


export const TablePage = ({headers, cities, currentlySelectedHeader}) => (
    <div>
        <h2>High-Rise Buildings</h2>
        <ReactTable
            showPagination={false}
            data={cities}
            columns={headers}
            pageSize={cities.length}
            noDataText="Loading..."
            sorted={[{
                id: currentlySelectedHeader,
                desc: false
            }]}
        />
    </div>
);