(function (global) {
  'use strict';

  const DEFAULT_REVIEWERS = ['Nikolaj', 'Toke', 'Marius', 'Mathias'];

  function getReviews(book) {
    const ratings = Array.isArray(book && book.ratings) ? book.ratings : [];
    const comments = Array.isArray(book && book.comments) ? book.comments : [];
    const reviewers = Array.isArray(book && book.reviewers)
      ? book.reviewers
      : DEFAULT_REVIEWERS;

    return ratings
      .map((rating, index) => ({
        reviewer: reviewers[index] || `Anmelder ${index + 1}`,
        rating: Number(rating),
        comment: comments[index] || ''
      }))
      .filter(review => Number.isFinite(review.rating));
  }

  function average(book) {
    const reviews = getReviews(book);
    if (reviews.length === 0) return null;
    return reviews.reduce((sum, review) => sum + review.rating, 0) / reviews.length;
  }

  function count(book) {
    return getReviews(book).length;
  }

  function reviewBy(book, reviewerName) {
    return getReviews(book).find(review => review.reviewer === reviewerName) || null;
  }

  function formatAverage(book, digits = 1) {
    const value = average(book);
    return value === null ? 'Ingen ratings' : `${value.toFixed(digits)}/10`;
  }

  global.BookRatings = Object.freeze({
    getReviews,
    average,
    count,
    reviewBy,
    formatAverage
  });
})(window);
