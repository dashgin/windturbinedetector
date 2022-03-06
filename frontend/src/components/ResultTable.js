import React from 'react'
import { Table } from 'antd';

const { Column, ColumnGroup } = Table;

const ResultTable = (data) => {
    let l = []
    const mappedData = data.data.map((item) => {
        l.push(item.data)
        console.log(item.data)
    })

    return (
        <Table dataSource={l} pagination={false}>
            <ColumnGroup title="Location">
                <Column title="Latitude" dataIndex="lat" />
                <Column title="Longtitude" dataIndex="long" />
            </ColumnGroup>
            <Column title="Intensity" dataIndex="intensity" />
            <Column title="Efficiency(kg/MJ)" dataIndex="efficiency" />
            <Column title="Type" dataIndex="turbine_type" />
            <Column title="Home Count" dataIndex="home_count_by_kwatt" />
            <Column title="Unit Price (AZN)" dataIndex="turbine_cost" />
            <Column title="Transportation Price (AZN)" dataIndex="turbine_transport_cost" />
        </Table>
    )
}

export default ResultTable