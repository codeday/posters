import React from 'react';
import Loading from './loading.js'


const Poster = (props) => {
    const regionNames = props.regions.map(region => region.name)

    if (regionNames.includes(props.posterRegion)) {
        return(
            <img src={`localhost:5000/generate/${props.posterRegion}/${props.posterTemplate}/${props.posterFormat}`}/>
        )
    } else {
        return(
            <p>Please use a Region from the List</p>
        )
    }
}

export default Poster