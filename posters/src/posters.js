import React,{useState} from 'react';
import EventDropdown from './eventDropdown.js';
import TemplateDropdown from './templateDropdown.js';
import Poster from './poster.js';
const Posters = () => {
    const [region, setRegion] = useState();
    return(
            <>
            <h1>CodeDay Poster Generator</h1>
                <EventDropdown setRegion={setRegion} />
                <Poster posterRegion={region} posterTemplate={"Blobs"} posterFormat={"svg"}/>
                </>
        )
}
export default Posters