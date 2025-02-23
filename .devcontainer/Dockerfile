FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm

ARG UV_ENV_FILE=.env

USER vscode
RUN pip install pre-commit

# zsh autocomplete (up/down arrows)
RUN git clone https://github.com/zsh-users/zsh-history-substring-search ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-history-substring-search
RUN echo "plugins=(git zsh-history-substring-search)" >> ~/.zshrc

RUN unset LOG_LEVEL
