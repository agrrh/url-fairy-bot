FROM alpine:latest
RUN echo \"* * * * * /bin/sh -c 'find /video_cache/ -type f -mmin +1440 -delete' > /etc/crontabs/root
CMD ["crond", "-f"]

