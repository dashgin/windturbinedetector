import React from "react";
import { Form, Input, Button, Space } from "antd";
import { MinusCircleOutlined, PlusOutlined } from "@ant-design/icons";
import axios from "axios";
import Map from "./Map";
import ResultTable from "./ResultTable";
import ResultChart from "./ResultChart";


const DynamicFieldSet = () => {
  const [data, setData] = React.useState([]);
  const [location, setLocation] = React.useState({});
  function getLocations(values) {
    axios({
      method: "POST",
      url: "http://localhost:8000/api/locations/",
      data: {
        locations: values.locations,
      }
    }).then((response) => {

      setData(response.data);
      setLocation(response.data[0].location);

    })
  }

  const onFinish = (values) => {
    getLocations(values);

  }

  const onFinishFailed = (values) => {
    console.log("Failed: ", values);
  };

  const staticValue = [
    { location: "40.6233,48.6543" },
    { location: "41.1952,47.1973" },
    { location: "40.6556,47.7466" },
    { location: "39.2206,45.4395" },
    { location: "40.1051,46.0396" },
  ];

  if (location?.length > 0) {
    return (
      <div className="row">
        <div className="col-6">

          <div className="row">
            <ResultTable data={data} />
          </div>
          <div className="row" style={{ maxWidth: "500px" }}>
            <ResultChart dataList={data[0].data} />
          </div>
        </div>
        <div className="col-6">
          <Map location={location} />
        </div>
      </div>
    )
  }
  return (

    <Form
      name="locationBase"
      onFinish={onFinish}
      onFinishFailed={onFinishFailed}
      autoComplete="on"
      className="col p-5"

    >

      <div className="border-l border-slate-900 mx-auto" >

        <Form.List name="locations"
          initialValue={staticValue}>

          {(fields, { add, remove }) => {
            return (
              <>
                <div>

                  {fields.map(({ key, name, ...restField }) => (
                    <Space
                      size={8}
                      key={key}
                      style={{
                        display: "flex",
                        marginBottom: 8
                      }}

                      align="baseline"
                    >

                      <Form.Item {...restField} name={[name, "location"]} className=" col-span-12 !mb-1">
                        <Input placeholder="Latitude,Longtitude" type="dashed"
                          className="h-full flex-1 !border !border-gray-900 focus:c-b-color" />
                      </Form.Item>
                      <MinusCircleOutlined onClick={() => remove(name)} />
                    </Space>
                  ))}
                </div>


                <Form.Item className="!mb-1">
                  <Button
                    onClick={() => add()}
                    block
                    className="h-full flex-1 !border !border-gray-900 focus:c-b-color"
                    icon={<PlusOutlined />}
                  >
                    Add location
                  </Button>
                </Form.Item>

                <Form.Item className="col-span-4 !mb-0">
                  <Button className="border border-gray-900 text-gray-900 rounded hover:bg-slate-900 hover:text-white" block htmlType="submit">
                    Detect
                  </Button>
                </Form.Item>
              </>
            )
          }}
        </Form.List>

      </div>
    </Form>

  );
};

export default DynamicFieldSet;