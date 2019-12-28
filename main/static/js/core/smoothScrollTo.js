/**
 * Performs a smooth scroll inside an element to a specific position, for a specific duration.
 * @param {Number} targetPosition - The position to scroll to.
 * @param {Number} duration - The duration of the animation, should be between 0 and 5000.
 * @return {Promise} Promise that will handle the smooth scroll.
 */
function smoothScrollTo(element, targetPosition = 0, duration = 500) {
  targetPosition = Math.round(targetPosition);
  duration = Math.round(duration);

  // Performs some validation on the duration value.
  if (duration < 0 || duration > 5000) {
    return Promise.reject(new Error('The duration must be comprised between 0 and 5000 ms.'));
  }

  // If the duration is set to 0, this means that we have to scroll to the target position without
  // animation.
  if (duration === 0) {
    element.scrollTop = targetPosition;
    return Promise.resolve();
  }

  // Sets start time and end time.
  const startTime = Date.now();
  const endTime = startTime + duration;

  // Computes the distance between the current number of pixels scrolled inside the considered
  // element and the target position.
  const initialScrollTop = element.scrollTop;
  const distance = targetPosition - initialScrollTop;

  // Defines a "smoothstep" function that'll be used to threshold the values of the number of pixels
  // scrolled and keep a smooth transition. In the context of a "smooth scroll" function, "start",
  // "end" and "point" correspond to times (in ms).
  const smoothStep = (start, end, point) => {
    if (point <= start) { return 0; }
    if (point >= end) { return 1; }
    // Computes linear interpolation.
    const x = (point - start) / (end - start);
    // Evaluates the "smoothstep" polynomial: smoothstep = 3x^2 - 2x^3.
    return x * x * (3 - (2 * x));
  };

  return new Promise((resolve) => {
    // Let's set the value of the current number of pixels scrolled.
    let currentScrollTop = element.scrollTop;

    // Defines a function that will handle the smooth scroll and update the scrollTop value of the
    // considered element.
    const scrollStep = () => {
      // Computes the new scrollTop value by ensuring a smooth transition.
      const now = Date.now();
      const point = smoothStep(startTime, endTime, now);
      const stepScrollTop = Math.round(initialScrollTop + (distance * point));
      element.scrollTop = stepScrollTop;

      // Are we done?
      if (now >= endTime) {
        resolve();
        return;
      }

      // If we were supposed to scroll but didn't, then we
      // probably hit the limit, so consider it done; not
      // interrupted.
      // Resolves the promise if we are still supposed to scroll according to the stepScrollTop
      // value but the scrollTop value won't move anymore.
      if (element.scrollTop === currentScrollTop && element.scrollTop !== stepScrollTop) {
        resolve();
        return;
      }

      // Update the current scrollTop value and schedule the next step.
      currentScrollTop = element.scrollTop;
      setTimeout(scrollStep, 0);
    };

    // Triggers the smooth scroll!
    setTimeout(scrollStep, 0);
  });
}

export default smoothScrollTo;
