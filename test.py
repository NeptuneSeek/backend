from utilities.scoring import ratings_reviews_scoring, availability_scoring



# rr_score = ratings_reviews_scoring(4.5, 100)
# print(f"Ratings and Reviews Score: {rr_score}")

# open_hours = [{'open': {'day': 1, 'hour': 7, 'minute': 0}, 'close': {'day': 1, 'hour': 21, 'minute': 0}}, {'open': {'day': 2, 'hour': 7, 'minute': 0}, 'close': {'day': 2, 'hour': 21, 'minute': 0}}, {'open': {'day': 3, 'hour': 7, 'minute': 0}, 'close': {'day': 3, 'hour': 21, 'minute': 0}}, {'open': {'day': 4, 'hour': 7, 'minute': 0}, 'close': {'day': 4, 'hour': 21, 'minute': 0}}, {'open': {'day': 5, 'hour': 7, 'minute': 0}, 'close': {'day': 5, 'hour': 21, 'minute': 0}}, {'open': {'day': 6, 'hour': 10, 'minute': 0}, 'close': {'day': 6, 'hour': 14, 'minute': 0}}]
# availability_score = availability_scoring(open_hours, True)
# print(f"Availability Score: {availability_score}")



import asyncio
async def async_test():
    from service.google import google_local_artisans

    results = await google_local_artisans("plumber", "Los Angeles, CA")
    print(results[2])
    # for res in results:
    #     print(res, end="\n\n")


asyncio.run(async_test())