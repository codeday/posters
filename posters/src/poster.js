import React from 'react';
import Loading from './loading.js'


const Poster = (props) => {
    const regionIds = props.regions.map(region => region.webname)

    if (regionIds.includes(props.posterRegion)) {
        return(
            <div className={"poster"}>
                <a href={`http://localhost:5000/generate/${props.posterRegion}/${props.posterTemplate}/pdf`} target="_self" download={`${props.posterRegion}_${props.posterTemplate}`}>
                    <img src={`http://localhost:5000/generate/${props.posterRegion}/${props.posterTemplate}/${props.posterFormat}`}/>
                </a>
            </div>
        )
    } else {
        return null
    }
}

export default Poster