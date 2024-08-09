# Use an appropriate base image based on your project's requirements
FROM golang:latest

# Set the working directory inside the container
WORKDIR /app

# Copy the Go module files
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy the rest of the source code
COPY . .
RUN go mod tidy
RUN apt-get update && apt-get install -y wireguard iproute2 netcat-traditional iputils-ping python3-scapy

# Build the project
RUN CGO_ENABLED=0 go build -v -trimpath -ldflags '-s -w' -o swgp-go ./cmd/swgp-go

# Run tests
#RUN go test -v -benchmem -bench . ./...

# You might want to add steps for uploading binaries as an artifact if needed

# Command to run the executable, you can adjust it according to your project
#CMD ["./swgp-go"]
