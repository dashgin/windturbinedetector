import React from 'react'
import { Layout, Menu, Breadcrumb, Row, Col } from 'antd';

import DynamicFieldSet from './DynamicFieldSet';

const { Header, Content, Footer } = Layout;

const Home = () => {
    return (

        <Content style={{ padding: '29px', minHeight: '86.7vh', backgroundColor: 'white' }}>
            <DynamicFieldSet />
        </Content>
    )
}

export default Home