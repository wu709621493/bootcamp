# Murphy’s Law: Why “Anything That Can Go Wrong” Feels So Right

## Core idea
Murphy’s Law is the observation that in complex systems, **small vulnerabilities eventually surface**, and if multiple failure paths exist, one of them will likely occur over time. It is less a prophecy of doom and more a reminder that **probability and complexity compound**.

## Why it seems true
- **Long time horizons**: With enough time, low-probability events stop being rare.
- **Hidden couplings**: Systems have dependencies you do not see until they break.
- **Biased recall**: We remember failures more vividly than the thousands of quiet successes.

## Engineering meaning
Murphy’s Law is a design directive:
- **Assume failure modes exist** before you see them.
- **Design for resilience** rather than perfect prevention.
- **Reduce blast radius** so one failure does not cascade.

## Practical checklist
1. **List failure modes**: Ask “How could this break?” for every subsystem.
2. **Stress test**: Simulate edge cases, overloads, and misuse.
3. **Add redundancy**: Duplicate critical components or pathways.
4. **Create clear fallbacks**: Safe defaults, circuit breakers, and timeouts.
5. **Monitor and learn**: Instrument systems; treat incidents as data.

## Everyday applications
- **Travel**: Build buffer time; one delay should not ruin the whole plan.
- **Projects**: Add risk buffers and define what “done” means early.
- **Health**: Small routines beat fragile grand plans.

## The optimistic twist
Murphy’s Law does not say everything will fail. It says **plan for how things fail** so that they can still succeed. It turns anxiety into preparation and turns bad surprises into survivable ones.
