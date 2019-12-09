import React from 'react';
import Loading from './loading.js'


const Poster = (props) => {
    return(
        <img src={`localhost:5000/generate/${props.posterRegion}/${props.posterTemplate}/${props.posterFormat}`}/>
    )
}

export default Poster