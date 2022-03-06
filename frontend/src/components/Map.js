import React from 'react'

const Map = ({ location }) => {
    return (
        <div dangerouslySetInnerHTML={
            { __html: `<iframe style="width:100%;height:80vh" src='https://maps.google.com/maps?q=${location[0]}, ${location[1]}&z=8&output=embed' frameborder='0' style='border:0'></iframe>` }
        } />
    )
}

export default Map