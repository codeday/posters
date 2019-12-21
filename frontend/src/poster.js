import React from 'react'

const Poster = props => {
  const regionIds = props.regions.map(region => region.webname)
  const promo = `promo=${encodeURIComponent(props.posterPromo)}&promoFor=${encodeURIComponent(props.posterPromoFor)}`;

  if (regionIds.includes(props.posterRegion)) {
    return (
      <div className='poster'>
        <a
          href={`render/${props.posterRegion}/${props.posterTemplate}/pdf?${promo}`}
          target="_self"
          download={`${props.posterRegion}_${props.posterTemplate}${props.posterPromo ? '_'+props.posterPromo : ''}.pdf`}
        >
          <img
            src={`/preview/${props.posterTemplate}.png`}
            style={{width: '300px'}}
          />
        </a>
        <br />
        <a
          class="downloadLink"
          href={`render/${props.posterRegion}/${props.posterTemplate}/png?${promo}`}
          target="_blank"
        >png</a>
        <a
          class="downloadLink"
          href={`render/${props.posterRegion}/${props.posterTemplate}/pdf?${promo}`}
          target="_self"
          download={`${props.posterRegion}_${props.posterTemplate}${props.posterPromo ? '_'+props.posterPromo : ''}.pdf`}
        >pdf</a>
      </div>
    )
  } else {
    return null
  }
}

export default Poster
